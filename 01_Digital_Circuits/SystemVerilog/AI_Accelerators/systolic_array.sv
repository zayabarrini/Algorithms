// Systolic array skeleton for matrix multiply (educational)
// This is a structural/behavioural skeleton showing dataflow and PE layout.
// Not fully optimized — intended as a clear starting point for FPGA implementation.

module systolic_array #(
    parameter DATA_W = 16,
    parameter DIM = 4
) (
    input  logic clk,
    input  logic rst_n,
    // Input streams for A (rows) and B (cols). Each call provides one column/row element.
    input  logic signed [DATA_W-1:0] a_in [DIM], // stream in per row
    input  logic signed [DATA_W-1:0] b_in [DIM], // stream in per column
    input  logic valid_in,
    output logic signed [2*DATA_W-1:0] c_out [DIM][DIM], // full result matrix when valid_out
    output logic valid_out
);

    // Internal signals between PEs (bundled)
    logic signed [DATA_W-1:0] a_out_sig [0:DIM-1][0:DIM-1];
    logic signed [DATA_W-1:0] b_out_sig [0:DIM-1][0:DIM-1];
    logic signed [2*DATA_W-1:0] acc_out_sig [0:DIM-1][0:DIM-1];
    logic valid_out_sig [0:DIM-1][0:DIM-1];
    logic ready_out_sig [0:DIM-1][0:DIM-1];

    // instantiate PEs using generate and hook up valid/ready handshakes
    genvar i, j;
    generate
        for (i = 0; i < DIM; i++) begin : row
            for (j = 0; j < DIM; j++) begin : col
                // local inputs to the PE: from left/up or top-level inputs
                logic signed [DATA_W-1:0] local_a_in;
                logic signed [DATA_W-1:0] local_b_in;
                logic signed [2*DATA_W-1:0] local_acc_in;
                logic local_valid_in;
                logic local_ready_in;

                // feed A into first column, otherwise from left PE's a_out
                if (j == 0) begin
                    assign local_a_in = a_in[i];
                end else begin
                    assign local_a_in = a_out_sig[i][j-1];
                end

                // feed B into first row, otherwise from above PE's b_out
                if (i == 0) begin
                    assign local_b_in = b_in[j];
                end else begin
                    assign local_b_in = b_out_sig[i-1][j];
                end

                // carry accumulator from left (start at zero for leftmost)
                if (j == 0) begin
                    assign local_acc_in = '0;
                end else begin
                    assign local_acc_in = acc_out_sig[i][j-1];
                end

                // valid_in comes from upstream PE's valid_out (or top-level)
                if (j == 0) begin
                    assign local_valid_in = valid_in;
                end else begin
                    assign local_valid_in = valid_out_sig[i][j-1];
                end

                // ready_in is taken from downstream PE's ready_out (or tied high at right edge)
                if (j == DIM-1) begin
                    assign local_ready_in = 1'b1; // rightmost column drains to top-level or memory
                end else begin
                    assign local_ready_in = ready_out_sig[i][j+1];
                end

                // instantiate PE with handshake
                pe #(.DATA_W(DATA_W)) pe_inst (
                    .clk(clk),
                    .rst_n(rst_n),
                    .a_in(local_a_in),
                    .b_in(local_b_in),
                    .acc_in(local_acc_in),
                    .valid_in(local_valid_in),
                    .ready_out(ready_out_sig[i][j]),
                    .a_out(a_out_sig[i][j]),
                    .b_out(b_out_sig[i][j]),
                    .acc_out(acc_out_sig[i][j]),
                    .valid_out(valid_out_sig[i][j]),
                    .ready_in(local_ready_in)
                );

                // expose final outputs from rightmost column
                if (j == DIM-1) begin
                    assign c_out[i][j] = acc_out_sig[i][j];
                end
            end
        end
    endgenerate

    // valid_out is asserted when bottom-right PE produces a valid bundle
    assign valid_out = valid_out_sig[DIM-1][DIM-1];

endmodule

// Notes:
// - This is a clearer, modular skeleton using a PE module and generate blocks.
// - For real synthesis: add handshake/ready, pipeline registers, memory interfaces
//   and proper control to stream A and B values at the required timing.
// - The accumulator width and fixed-point format need careful design for overflow.

