`timescale 1ns/1ps

package dsp_mapping_pkg;
    typedef enum logic [1:0] {
        INTERLEAVED_MAP = 2'b00,
        BLOCKED_MAP     = 2'b01,
        BANK_CONS_MAP   = 2'b10,
        ADAPTIVE_MAP    = 2'b11
    } mapping_mode_t;
    
    typedef struct packed {
        logic [15:0] block_id;
        logic [7:0]  memory_bank;
        logic [7:0]  cache_line;
        logic [31:0] base_address;
        logic        valid;
    } block_mapping_t;
    
    typedef struct packed {
        logic [7:0]  num_memory_banks;
        logic [7:0]  cache_lines_per_bank;
        logic [15:0] block_size_bytes;
        logic [15:0] max_blocks;
    } system_config_t;
endpackage

module dsp_block_mapping #(
    parameter NUM_BANKS         = 8,
    parameter CACHE_LINES       = 16,
    parameter BLOCK_SIZE_BYTES  = 64,
    parameter ADDR_WIDTH        = 32,
    parameter BLOCK_ID_WIDTH    = 16
)(
    input  logic                         clk,
    input  logic                         rst_n,
    
    // Configuration interface
    input  dsp_mapping_pkg::mapping_mode_t map_mode,
    input  dsp_mapping_pkg::system_config_t sys_config,
    
    // Block mapping request interface
    input  logic                         map_req_valid,
    input  logic [BLOCK_ID_WIDTH-1:0]    block_id,
    input  logic [ADDR_WIDTH-1:0]        base_addr,
    output logic                         map_ready,
    
    // Mapping result interface
    output dsp_mapping_pkg::block_mapping_t mapping_result,
    output logic                         map_result_valid,
    input  logic                         map_result_ready,
    
    // Performance monitoring
    output logic [31:0]                  bank_conflict_count,
    output logic [31:0]                  cache_miss_count
);
    
    import dsp_mapping_pkg::*;
    
    // Internal signals
    logic [7:0] calculated_bank;
    logic [7:0] calculated_cache_line;
    logic [ADDR_WIDTH-1:0] calculated_addr;
    logic mapping_valid;
    
    // Bank conflict detection
    logic [NUM_BANKS-1:0] bank_access_history;
    logic bank_conflict_detected;
    
    // Cache performance tracking
    logic [CACHE_LINES-1:0] cache_line_history;
    logic cache_miss_detected;
    
    // =========================================================================
    // Interleaved Mapping Implementation
    // =========================================================================
    function automatic logic [7:0] interleaved_mapping(
        input logic [BLOCK_ID_WIDTH-1:0] block_id,
        input logic [7:0] num_banks
    );
        return block_id % num_banks;
    endfunction
    
    // =========================================================================
    // Blocked Mapping Implementation  
    // =========================================================================
    function automatic logic [7:0] blocked_mapping(
        input logic [BLOCK_ID_WIDTH-1:0] block_id,
        input logic [7:0] num_banks,
        input logic [15:0] block_stride
    );
        logic [15:0] block_group;
        block_group = block_id / block_stride;
        return block_group % num_banks;
    endfunction
    
    // =========================================================================
    // Cache Line Calculation
    // =========================================================================
    function automatic logic [7:0] calculate_cache_line(
        input logic [BLOCK_ID_WIDTH-1:0] block_id,
        input logic [ADDR_WIDTH-1:0] base_addr,
        input logic [15:0] block_size
    );
        logic [ADDR_WIDTH-1:0] block_addr;
        block_addr = base_addr + (block_id * block_size);
        return block_addr[7:0] % CACHE_LINES; // Simple modulo for demo
    endfunction
    
    // =========================================================================
    // Address Calculation
    // =========================================================================
    function automatic logic [ADDR_WIDTH-1:0] calculate_base_address(
        input logic [BLOCK_ID_WIDTH-1:0] block_id,
        input logic [ADDR_WIDTH-1:0] system_base,
        input logic [15:0] block_size
    );
        return system_base + (block_id * block_size);
    endfunction
    
    // =========================================================================
    // Main Mapping FSM
    // =========================================================================
    typedef enum logic [2:0] {
        IDLE        = 3'b000,
        CALC_BANK   = 3'b001,
        CALC_CACHE  = 3'b010,
        CHECK_CONF  = 3'b011,
        OUTPUT_MAP  = 3'b100,
        WAIT_READY  = 3'b101
    } mapping_state_t;
    
    mapping_state_t current_state, next_state;
    
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            current_state <= IDLE;
        end else begin
            current_state <= next_state;
        end
    end
    
    // Next state logic
    always_comb begin
        next_state = current_state;
        
        case (current_state)
            IDLE: begin
                if (map_req_valid && map_ready) begin
                    next_state = CALC_BANK;
                end
            end
            
            CALC_BANK: begin
                next_state = CALC_CACHE;
            end
            
            CALC_CACHE: begin
                next_state = CHECK_CONF;
            end
            
            CHECK_CONF: begin
                next_state = OUTPUT_MAP;
            end
            
            OUTPUT_MAP: begin
                if (map_result_ready) begin
                    next_state = IDLE;
                end else begin
                    next_state = WAIT_READY;
                end
            end
            
            WAIT_READY: begin
                if (map_result_ready) begin
                    next_state = IDLE;
                end
            end
            
            default: next_state = IDLE;
        endcase
    end
    
    // Control signals
    assign map_ready = (current_state == IDLE);
    
    // =========================================================================
    // Mapping Calculation Pipeline
    // =========================================================================
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            calculated_bank      <= '0;
            calculated_cache_line <= '0;
            calculated_addr      <= '0;
            mapping_valid        <= '0;
            mapping_result       <= '0;
        end else begin
            case (current_state)
                CALC_BANK: begin
                    // Calculate memory bank based on mapping mode
                    case (map_mode)
                        INTERLEAVED_MAP: begin
                            calculated_bank <= interleaved_mapping(
                                block_id, sys_config.num_memory_banks
                            );
                        end
                        
                        BLOCKED_MAP: begin
                            calculated_bank <= blocked_mapping(
                                block_id, 
                                sys_config.num_memory_banks,
                                sys_config.block_size_bytes
                            );
                        end
                        
                        default: begin
                            calculated_bank <= interleaved_mapping(
                                block_id, sys_config.num_memory_banks
                            );
                        end
                    endcase
                    
                    // Calculate base address
                    calculated_addr <= calculate_base_address(
                        block_id, base_addr, sys_config.block_size_bytes
                    );
                end
                
                CALC_CACHE: begin
                    calculated_cache_line <= calculate_cache_line(
                        block_id, calculated_addr, sys_config.block_size_bytes
                    );
                end
                
                OUTPUT_MAP: begin
                    mapping_result.block_id      <= block_id;
                    mapping_result.memory_bank   <= calculated_bank;
                    mapping_result.cache_line    <= calculated_cache_line;
                    mapping_result.base_address  <= calculated_addr;
                    mapping_result.valid         <= 1'b1;
                    mapping_valid <= 1'b1;
                end
                
                WAIT_READY: begin
                    // Hold values until ready
                end
                
                default: begin
                    mapping_valid <= 1'b0;
                    mapping_result.valid <= 1'b0;
                end
            endcase
        end
    end
    
    assign map_result_valid = mapping_valid;
    
    // =========================================================================
    // Bank Conflict Detection
    // =========================================================================
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            bank_access_history <= '0;
            bank_conflict_count <= '0;
        end else if (map_result_valid && map_result_ready) begin
            // Check if this bank was recently accessed
            bank_conflict_detected = bank_access_history[calculated_bank];
            
            // Update history - set bit for current bank
            bank_access_history <= (1 << calculated_bank);
            
            // Count conflicts
            if (bank_conflict_detected) begin
                bank_conflict_count <= bank_conflict_count + 1;
            end
        end
    end
    
    // =========================================================================
    // Cache Performance Monitoring
    // =========================================================================
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cache_line_history <= '0;
            cache_miss_count   <= '0;
        end else if (map_result_valid && map_result_ready) begin
            // Simple cache miss detection
            cache_miss_detected = ~cache_line_history[calculated_cache_line];
            
            // Update cache line history
            cache_line_history[calculated_cache_line] <= 1'b1;
            
            // Count misses
            if (cache_miss_detected) begin
                cache_miss_count <= cache_miss_count + 1;
            end
        end
    end
    
    // =========================================================================
    // Assertions for Correctness
    // =========================================================================
    `ifndef SYNTHESIS
    // Precondition: Memory banks must be power of 2
    property power_of_two_banks;
        @(posedge clk) disable iff (!rst_n)
        (sys_config.num_memory_banks & (sys_config.num_memory_banks - 1)) == 0;
    endproperty
    assert_power_of_two_banks: assert property (power_of_two_banks)
        else $error("Memory banks must be power of 2");
    
    // Postcondition: Valid mapping output
    property valid_mapping_output;
        @(posedge clk) disable iff (!rst_n)
        (map_result_valid) |-> (mapping_result.valid && 
                               (mapping_result.memory_bank < NUM_BANKS) &&
                               (mapping_result.cache_line < CACHE_LINES));
    endproperty
    assert_valid_mapping: assert property (valid_mapping_output)
        else $error("Invalid mapping output");
    
    // Edge case: Single block mapping
    property single_block_mapping;
        @(posedge clk) disable iff (!rst_n)
        (map_req_valid && (sys_config.max_blocks == 1)) |-> 
        ##3 (map_result_valid && (mapping_result.memory_bank == 0));
    endproperty
    `endif
    
endmodule

module memory_bank_controller #(
    parameter NUM_BANKS        = 8,
    parameter BANK_DEPTH       = 1024,
    parameter DATA_WIDTH       = 64,
    parameter ADDR_WIDTH       = 32
)(
    input  logic                         clk,
    input  logic                         rst_n,
    
    // Bank access interface
    input  logic [NUM_BANKS-1:0]         bank_request,
    input  logic [ADDR_WIDTH-1:0]        bank_addr [NUM_BANKS],
    input  logic                         bank_write [NUM_BANKS],
    input  logic [DATA_WIDTH-1:0]        bank_wdata [NUM_BANKS],
    output logic [DATA_WIDTH-1:0]        bank_rdata [NUM_BANKS],
    output logic [NUM_BANKS-1:0]         bank_ready,
    
    // Arbitration and performance
    output logic [7:0]                   active_bank,
    output logic                         arbitration_conflict,
    output logic [31:0]                  access_count [NUM_BANKS]
);
    
    // Bank memory arrays
    logic [DATA_WIDTH-1:0] bank_memory [NUM_BANKS][BANK_DEPTH];
    
    // Bank state machines
    typedef enum logic [1:0] {
        BANK_IDLE    = 2'b00,
        BANK_READ    = 2'b01,
        BANK_WRITE   = 2'b10,
        BANK_WAIT    = 2'b11
    } bank_state_t;
    
    bank_state_t bank_state [NUM_BANKS];
    logic [7:0] bank_latency_counter [NUM_BANKS];
    
    // Bank arbitration
    logic [NUM_BANKS-1:0] bank_grant;
    logic arbitration_active;
    
    // =========================================================================
    // Round-robin Arbiter
    // =========================================================================
    rr_arbiter #(.WIDTH(NUM_BANKS)) bank_arbiter (
        .clk(clk),
        .rst_n(rst_n),
        .request(bank_request),
        .grant(bank_grant),
        .any_grant(arbitration_active)
    );
    
    // =========================================================================
    // Bank Controller FSM
    // =========================================================================
    genvar i;
    generate
        for (i = 0; i < NUM_BANKS; i++) begin : bank_controllers
            always_ff @(posedge clk or negedge rst_n) begin
                if (!rst_n) begin
                    bank_state[i] <= BANK_IDLE;
                    bank_latency_counter[i] <= '0;
                    bank_ready[i] <= 1'b0;
                    bank_rdata[i] <= '0;
                    access_count[i] <= '0;
                end else begin
                    case (bank_state[i])
                        BANK_IDLE: begin
                            bank_ready[i] <= 1'b1;
                            
                            if (bank_request[i] && bank_grant[i]) begin
                                bank_state[i] <= bank_write[i] ? BANK_WRITE : BANK_READ;
                                bank_ready[i] <= 1'b0;
                                bank_latency_counter[i] <= 3; // 3-cycle latency
                                access_count[i] <= access_count[i] + 1;
                            end
                        end
                        
                        BANK_READ: begin
                            if (bank_latency_counter[i] == 0) begin
                                bank_rdata[i] <= bank_memory[i][bank_addr[i][$clog2(BANK_DEPTH)-1:0]];
                                bank_state[i] <= BANK_WAIT;
                            end else begin
                                bank_latency_counter[i] <= bank_latency_counter[i] - 1;
                            end
                        end
                        
                        BANK_WRITE: begin
                            if (bank_latency_counter[i] == 0) begin
                                bank_memory[i][bank_addr[i][$clog2(BANK_DEPTH)-1:0]] <= bank_wdata[i];
                                bank_state[i] <= BANK_WAIT;
                            end else begin
                                bank_latency_counter[i] <= bank_latency_counter[i] - 1;
                            end
                        end
                        
                        BANK_WAIT: begin
                            bank_state[i] <= BANK_IDLE;
                            bank_ready[i] <= 1'b1;
                        end
                    endcase
                end
            end
        end
    endgenerate
    
    // =========================================================================
    // Conflict Detection
    // =========================================================================
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            arbitration_conflict <= 1'b0;
            active_bank <= '0;
        end else begin
            // Detect multiple simultaneous requests
            arbitration_conflict <= (|bank_request) && (bank_request & (bank_request - 1)) != 0;
            
            // Track active bank
            for (int j = 0; j < NUM_BANKS; j++) begin
                if (bank_grant[j]) begin
                    active_bank <= j;
                end
            end
        end
    end
    
endmodule

// Round-robin arbiter module
module rr_arbiter #(
    parameter WIDTH = 8
)(
    input  logic             clk,
    input  logic             rst_n,
    input  logic [WIDTH-1:0] request,
    output logic [WIDTH-1:0] grant,
    output logic             any_grant
);
    
    logic [WIDTH-1:0] pointer;
    logic [WIDTH-1:0] mask_higher_pri;
    logic [WIDTH-1:0] grant_masked;
    logic [WIDTH-1:0] grant_unmasked;
    
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pointer <= {{(WIDTH-1){1'b0}}, 1'b1}; // Start at LSB
        end else if (any_grant) begin
            // Rotate pointer to next granted position
            pointer <= {grant[WIDTH-2:0], grant[WIDTH-1]};
        end
    end
    
    // Mask higher priority requests based on pointer
    assign mask_higher_pri = ~((1 << pointer) - 1);
    assign grant_masked = request & mask_higher_pri;
    assign grant_unmasked = request & ~mask_higher_pri;
    
    // Grant calculation
    assign grant = grant_masked != 0 ? 
                  grant_masked & -grant_masked : // Find first set in masked
                  grant_unmasked & -grant_unmasked; // Find first set in unmasked
    
    assign any_grant = |request;
    
endmodule

module cache_aware_mapper #(
    parameter CACHE_SETS         = 64,
    parameter CACHE_WAYS         = 4,
    parameter CACHE_LINE_SIZE    = 64,
    parameter ADDR_WIDTH         = 32
)(
    input  logic                         clk,
    input  logic                         rst_n,
    
    // Cache configuration
    input  logic [15:0]                  cache_size_bytes,
    input  logic [7:0]                   cache_associativity,
    
    // Mapping requests
    input  logic                         map_req_valid,
    input  logic [ADDR_WIDTH-1:0]        physical_addr,
    input  logic [15:0]                  block_size,
    output logic [15:0]                  optimal_block_stride,
    output logic                         map_ready,
    
    // Cache performance hints
    output logic                         cache_friendly,
    output logic [7:0]                   expected_cache_hits,
    output logic [3:0]                   spatial_locality_score
);
    
    // Cache set calculation
    function automatic logic [15:0] calculate_cache_set(
        input logic [ADDR_WIDTH-1:0] addr
    );
        logic [ADDR_WIDTH-1:0] cache_line_addr;
        cache_line_addr = addr / CACHE_LINE_SIZE;
        return cache_line_addr % CACHE_SETS;
    endfunction
    
    // Optimal stride calculation
    function automatic logic [15:0] calculate_optimal_stride(
        input logic [15:0] block_size,
        input logic [15:0] cache_size,
        input logic [7:0]  associativity
    );
        logic [15:0] stride;
        // Avoid cache thrashing - ensure blocks don't alias
        stride = cache_size / (associativity * 4); // Conservative factor
        stride = (stride / block_size) * block_size; // Align to block size
        return stride > 0 ? stride : block_size;
    endfunction
    
    // Spatial locality analysis
    function automatic logic [3:0] analyze_spatial_locality(
        input logic [ADDR_WIDTH-1:0] addr,
        input logic [15:0] block_size
    );
        logic [3:0] score;
        // Simple heuristic based on block size and typical access patterns
        if (block_size <= 16) score = 2;  // Small blocks - poor locality
        else if (block_size <= 64) score = 5; // Medium blocks
        else if (block_size <= 256) score = 8; // Large blocks - good locality
        else score = 10; // Very large blocks - excellent locality
        return score;
    endfunction
    
    // Cache hit prediction
    function automatic logic [7:0] predict_cache_hits(
        input logic [3:0] locality_score,
        input logic [15:0] stride
    );
        logic [7:0] hits;
        // Simple model: higher locality + optimal stride = more hits
        hits = (locality_score * 5) + (stride == optimal_block_stride ? 20 : 0);
        return hits > 100 ? 100 : hits; // Cap at 100%
    endfunction
    
    // Internal registers
    logic [15:0] current_stride;
    logic [3:0] current_locality;
    logic cache_analysis_valid;
    
    // =========================================================================
    // Main Analysis FSM
    // =========================================================================
    typedef enum logic [1:0] {
        CA_IDLE      = 2'b00,
        CA_ANALYZE   = 2'b01,
        CA_CALCULATE = 2'b10,
        CA_OUTPUT    = 2'b11
    } cache_analysis_state_t;
    
    cache_analysis_state_t ca_state;
    
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ca_state <= CA_IDLE;
            optimal_block_stride <= '0;
            cache_friendly <= 1'b0;
            expected_cache_hits <= '0;
            spatial_locality_score <= '0;
            cache_analysis_valid <= 1'b0;
        end else begin
            case (ca_state)
                CA_IDLE: begin
                    cache_analysis_valid <= 1'b0;
                    if (map_req_valid && map_ready) begin
                        ca_state <= CA_ANALYZE;
                    end
                end
                
                CA_ANALYZE: begin
                    // Analyze spatial locality
                    current_locality <= analyze_spatial_locality(physical_addr, block_size);
                    ca_state <= CA_CALCULATE;
                end
                
                CA_CALCULATE: begin
                    // Calculate optimal stride
                    current_stride <= calculate_optimal_stride(
                        block_size, cache_size_bytes, cache_associativity
                    );
                    ca_state <= CA_OUTPUT;
                end
                
                CA_OUTPUT: begin
                    optimal_block_stride <= current_stride;
                    spatial_locality_score <= current_locality;
                    expected_cache_hits <= predict_cache_hits(current_locality, current_stride);
                    cache_friendly <= (current_locality >= 6); // Threshold for "friendly"
                    cache_analysis_valid <= 1'b1;
                    ca_state <= CA_IDLE;
                end
            endcase
        end
    end
    
    assign map_ready = (ca_state == CA_IDLE);
    
endmodule

module dsp_performance_monitor #(
    parameter NUM_BANKS        = 8,
    parameter NUM_METRICS      = 16
)(
    input  logic                         clk,
    input  logic                         rst_n,
    
    // Performance events
    input  logic                         bank_conflict_event,
    input  logic                         cache_miss_event,
    input  logic                         mapping_complete_event,
    input  logic [7:0]                   active_bank,
    input  logic                         arbitration_conflict,
    
    // Configuration
    input  logic [31:0]                  sample_interval,
    input  logic                         continuous_monitoring,
    
    // Performance counters output
    output logic [31:0]                  bank_conflict_count,
    output logic [31:0]                  cache_miss_count,
    output logic [31:0]                  total_mappings,
    output logic [31:0]                  bank_utilization [NUM_BANKS],
    output logic [7:0]                   average_latency,
    output logic                         performance_alert
);
    
    // Performance counters
    logic [31:0] conflict_counter;
    logic [31:0] miss_counter;
    logic [31:0] mapping_counter;
    logic [31:0] bank_counters [NUM_BANKS];
    logic [31:0] latency_accumulator;
    logic [31:0] latency_samples;
    
    // Timing control
    logic [31:0] sample_timer;
    logic sample_period_complete;
    
    // Alert thresholds
    localparam CONFLICT_THRESHOLD = 1000;
    localparam MISS_THRESHOLD = 5000;
    localparam UTILIZATION_THRESHOLD = 90; // Percentage
    
    // =========================================================================
    // Event Counting
    // =========================================================================
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            conflict_counter <= '0;
            miss_counter <= '0;
            mapping_counter <= '0;
            for (int i = 0; i < NUM_BANKS; i++) begin
                bank_counters[i] <= '0;
            end
            latency_accumulator <= '0;
            latency_samples <= '0;
        end else begin
            // Count bank conflicts
            if (bank_conflict_event) begin
                conflict_counter <= conflict_counter + 1;
            end
            
            // Count cache misses
            if (cache_miss_event) begin
                miss_counter <= miss_counter + 1;
            end
            
            // Count total mappings
            if (mapping_complete_event) begin
                mapping_counter <= mapping_counter + 1;
                bank_counters[active_bank] <= bank_counters[active_bank] + 1;
            end
            
            // Simple latency tracking (in cycles)
            if (mapping_complete_event) begin
                // This would normally come from actual latency measurement
                latency_accumulator <= latency_accumulator + 5; // Example: 5 cycles
                latency_samples <= latency_samples + 1;
            end
        end
    end
    
    // =========================================================================
    // Sampling Timer
    // =========================================================================
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sample_timer <= '0;
            sample_period_complete <= 1'b0;
        end else begin
            if (sample_timer >= sample_interval) begin
                sample_timer <= '0;
                sample_period_complete <= 1'b1;
            end else begin
                sample_timer <= sample_timer + 1;
                sample_period_complete <= 1'b0;
            end
        end
    end
    
    // =========================================================================
    // Statistics Calculation
    // =========================================================================
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            bank_conflict_count <= '0;
            cache_miss_count <= '0;
            total_mappings <= '0;
            for (int i = 0; i < NUM_BANKS; i++) begin
                bank_utilization[i] <= '0;
            end
            average_latency <= '0;
            performance_alert <= 1'b0;
        end else if (sample_period_complete || continuous_monitoring) begin
            // Update output counters
            bank_conflict_count <= conflict_counter;
            cache_miss_count <= miss_counter;
            total_mappings <= mapping_counter;
            
            // Calculate bank utilization percentages
            for (int i = 0; i < NUM_BANKS; i++) begin
                if (mapping_counter > 0) begin
                    bank_utilization[i] <= (bank_counters[i] * 100) / mapping_counter;
                end else begin
                    bank_utilization[i] <= '0;
                end
            end
            
            // Calculate average latency
            if (latency_samples > 0) begin
                average_latency <= latency_accumulator / latency_samples;
            end
            
            // Performance alerts
            performance_alert <= (conflict_counter > CONFLICT_THRESHOLD) ||
                               (miss_counter > MISS_THRESHOLD) ||
                               (bank_utilization[0] > UTILIZATION_THRESHOLD); // Check first bank as example
        end
    end
    
endmodule

module dsp_block_mapping_tb;
    import dsp_mapping_pkg::*;
    
    // Parameters
    localparam CLK_PERIOD = 10;
    localparam NUM_TEST_BLOCKS = 100;
    
    // Clock and reset
    logic clk;
    logic rst_n;
    
    // DUT interfaces
    mapping_mode_t map_mode;
    system_config_t sys_config;
    logic map_req_valid;
    logic [15:0] block_id;
    logic [31:0] base_addr;
    logic map_ready;
    block_mapping_t mapping_result;
    logic map_result_valid;
    logic map_result_ready;
    
    // Test variables
    int mapping_latency [NUM_TEST_BLOCKS];
    int bank_distribution [8]; // 8 banks
    int test_pass_count;
    int test_fail_count;
    
    // Clock generation
    initial begin
        clk = 0;
        forever #(CLK_PERIOD/2) clk = ~clk;
    end
    
    // Reset generation
    initial begin
        rst_n = 0;
        #100 rst_n = 1;
    end
    
    // DUT instantiation
    dsp_block_mapping #(
        .NUM_BANKS(8),
        .CACHE_LINES(16),
        .BLOCK_SIZE_BYTES(64),
        .ADDR_WIDTH(32),
        .BLOCK_ID_WIDTH(16)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .map_mode(map_mode),
        .sys_config(sys_config),
        .map_req_valid(map_req_valid),
        .block_id(block_id),
        .base_addr(base_addr),
        .map_ready(map_ready),
        .mapping_result(mapping_result),
        .map_result_valid(map_result_valid),
        .map_result_ready(map_result_ready),
        .bank_conflict_count(),
        .cache_miss_count()
    );
    
    // Test sequence
    initial begin
        initialize_test();
        
        // Test 1: Interleaved mapping
        $display("=== Test 1: Interleaved Mapping ===");
        map_mode = INTERLEAVED_MAP;
        run_mapping_test(0, 99);
        
        // Test 2: Blocked mapping  
        $display("=== Test 2: Blocked Mapping ===");
        map_mode = BLOCKED_MAP;
        run_mapping_test(0, 99);
        
        // Test 3: Edge cases
        $display("=== Test 3: Edge Cases ===");
        test_edge_cases();
        
        print_test_results();
        $finish;
    end
    
    task initialize_test();
        // Initialize system configuration
        sys_config.num_memory_banks = 8;
        sys_config.cache_lines_per_bank = 16;
        sys_config.block_size_bytes = 64;
        sys_config.max_blocks = 1000;
        
        // Initialize test counters
        test_pass_count = 0;
        test_fail_count = 0;
        for (int i = 0; i < 8; i++) bank_distribution[i] = 0;
        
        map_req_valid = 0;
        map_result_ready = 1;
        base_addr = 32'h1000_0000;
        
        wait(rst_n);
        #100;
    endtask
    
    task run_mapping_test(input int start_id, input int end_id);
        automatic int start_time, end_time, latency;
        
        for (int i = start_id; i <= end_id; i++) begin
            // Wait for mapper to be ready
            wait(map_ready);
            
            // Send mapping request
            start_time = $time;
            block_id = i;
            map_req_valid = 1;
            
            @(posedge clk);
            map_req_valid = 0;
            
            // Wait for result
            wait(map_result_valid);
            end_time = $time;
            
            // Record latency
            latency = (end_time - start_time) / CLK_PERIOD;
            mapping_latency[i] = latency;
            
            // Record bank distribution
            bank_distribution[mapping_result.memory_bank]++;
            
            // Verify mapping correctness
            verify_mapping(i, mapping_result);
            
            @(posedge clk);
        end
        
        analyze_performance(start_id, end_id);
    endtask
    
    task verify_mapping(input int expected_id, input block_mapping_t result);
        automatic logic [7:0] expected_bank;
        
        // Calculate expected bank based on mapping mode
        case (map_mode)
            INTERLEAVED_MAP: expected_bank = expected_id % sys_config.num_memory_banks;
            BLOCKED_MAP: expected_bank = (expected_id / sys_config.block_size_bytes) % sys_config.num_memory_banks;
            default: expected_bank = expected_id % sys_config.num_memory_banks;
        endcase
        
        if (result.memory_bank == expected_bank && 
            result.block_id == expected_id &&
            result.valid) begin
            test_pass_count++;
            $display("PASS: Block %0d -> Bank %0d", expected_id, result.memory_bank);
        end else begin
            test_fail_count++;
            $error("FAIL: Block %0d -> Bank %0d (expected %0d)", 
                   expected_id, result.memory_bank, expected_bank);
        end
    endtask
    
    task test_edge_cases();
        $display("Testing single block...");
        run_mapping_test(0, 0);
        
        $display("Testing power-of-2 boundary...");
        run_mapping_test(62, 66); // Around 64
        
        $display("Testing bank boundary...");
        run_mapping_test(6, 9); // Around bank count
    endtask
    
    task analyze_performance(input int start_id, input int end_id);
        automatic int total_latency = 0;
        automatic int min_latency = 999;
        automatic int max_latency = 0;
        
        for (int i = start_id; i <= end_id; i++) begin
            total_latency += mapping_latency[i];
            if (mapping_latency[i] < min_latency) min_latency = mapping_latency[i];
            if (mapping_latency[i] > max_latency) max_latency = mapping_latency[i];
        end
        
        $display("Performance Analysis:");
        $display("  Total blocks mapped: %0d", (end_id - start_id + 1));
        $display("  Average latency: %0d cycles", total_latency / (end_id - start_id + 1));
        $display("  Min latency: %0d cycles", min_latency);
        $display("  Max latency: %0d cycles", max_latency);
        $display("  Bank distribution: %p", bank_distribution);
    endtask
    
    task print_test_results();
        $display("\n=== TEST RESULTS ===");
        $display("Passed: %0d", test_pass_count);
        $display("Failed: %0d", test_fail_count);
        $display("Total:  %0d", test_pass_count + test_fail_count);
        
        if (test_fail_count == 0) begin
            $display("*** ALL TESTS PASSED ***");
        end else begin
            $display("*** SOME TESTS FAILED ***");
        end
    endtask
    
    // Monitoring
    always @(posedge clk) begin
        if (map_result_valid) begin
            $display("Time %0t: Mapping complete - Block %0d -> Bank %0d, Cache Line %0d",
                     $time, mapping_result.block_id, mapping_result.memory_bank, 
                     mapping_result.cache_line);
        end
    end
    
endmodule