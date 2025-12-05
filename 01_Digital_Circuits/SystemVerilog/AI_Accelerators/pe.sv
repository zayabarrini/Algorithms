// Processing Element (PE) for a systolic array multiply-accumulate
module pe #(
    parameter DATA_W = 16
) (
    input  logic clk,
    input  logic rst_n,
    // data inputs
    input  logic signed [DATA_W-1:0] a_in,
    input  logic signed [DATA_W-1:0] b_in,
    input  logic signed [2*DATA_W-1:0] acc_in,
    input  logic valid_in,
    output logic signed [DATA_W-1:0] a_out,
    output logic signed [DATA_W-1:0] b_out,
    output logic signed [2*DATA_W-1:0] acc_out,
    output logic valid_out
);

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            a_out <= '0;
            b_out <= '0;
            acc_out <= '0;
            valid_out <= 0;
        end else begin
            // pass a/b to the right/bottom neighbors on next cycle
            a_out <= a_in;
            b_out <= b_in;
            // multiply-accumulate
            acc_out <= acc_in + $signed(a_in) * $signed(b_in);
            valid_out <= valid_in;

        module pe #(
            parameter DATA_W = 16
        ) (
            input  logic clk,
            input  logic rst_n,
            // bundled data inputs/outputs (a,b,acc)
            input  logic signed [DATA_W-1:0] a_in,
            input  logic signed [DATA_W-1:0] b_in,
            input  logic signed [2*DATA_W-1:0] acc_in,
            input  logic valid_in,            // indicates input bundle is valid
            output logic ready_out,           // indicates PE can accept upstream data

            output logic signed [DATA_W-1:0] a_out,
            output logic signed [DATA_W-1:0] b_out,
            output logic signed [2*DATA_W-1:0] acc_out,
            output logic valid_out,           // output bundle valid
            input  logic ready_in             // downstream ready signal
        );

            // Two-stage pipeline registers
            logic reg_valid0, reg_valid1;
            logic signed [DATA_W-1:0] a0, b0, a1, b1;
            logic signed [2*DATA_W-1:0] acc0, acc1;

            // Ready: can accept new input if both pipeline stages are not full
            assign ready_out = !(reg_valid0 && reg_valid1);

            // Output driven from stage1
            assign valid_out = reg_valid1;
            assign a_out = a1;
            assign b_out = b1;
            assign acc_out = acc1;

            always_ff @(posedge clk or negedge rst_n) begin
                if (!rst_n) begin
                    reg_valid0 <= 0;
                    reg_valid1 <= 0;
                    a0 <= '0; b0 <= '0; acc0 <= '0;
                    a1 <= '0; b1 <= '0; acc1 <= '0;
                end else begin
                    // If stage1 has valid and downstream is ready, consume stage1
                    if (reg_valid1 && ready_in) begin
                        reg_valid1 <= 0;
                    end

                    // Move stage0 -> stage1 if stage0 is valid and stage1 is free
                    if (reg_valid0 && !reg_valid1) begin
                        reg_valid1 <= 1;
                        a1 <= a0;
                        b1 <= b0;
                        acc1 <= acc0 + $signed(a0) * $signed(b0);
                        reg_valid0 <= 0;
                    end

                    // Capture new input into stage0 when available and stage0 free
                    if (valid_in && ready_out) begin
                        reg_valid0 <= 1;
                        a0 <= a_in;
                        b0 <= b_in;
                        acc0 <= acc_in;
                    end
                end
            end

        endmodule
