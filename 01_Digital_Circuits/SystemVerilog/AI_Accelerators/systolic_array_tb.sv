`timescale 1ns/1ps
module tb_systolic;
    parameter DATA_W = 16;
    parameter DIM = 3;

    logic clk;
    logic rst_n;
    logic signed [DATA_W-1:0] a_in [DIM];
    logic signed [DATA_W-1:0] b_in [DIM];
    logic valid_in;
    logic signed [2*DATA_W-1:0] c_out [DIM][DIM];
    logic valid_out;

    // Clock
    initial clk = 0; always #5 clk = ~clk;

    // instantiate
    systolic_array #(.DATA_W(DATA_W), .DIM(DIM)) dut (
        .clk(clk),
        .rst_n(rst_n),
        .a_in(a_in),
        .b_in(b_in),
        .valid_in(valid_in),
        .c_out(c_out),
        .valid_out(valid_out)
    );

    initial begin
        rst_n = 0;
        valid_in = 0;
        repeat (2) @(posedge clk);
        rst_n = 1;

        // example matrices (rows streamed in as a_in per cycle, columns streamed as b_in)
        a_in[0] = 1; a_in[1] = 4; a_in[2] = 7;
        b_in[0] = 9; b_in[1] = 6; b_in[2] = 3;
        valid_in = 1;
        @(posedge clk);

        a_in[0] = 2; a_in[1] = 5; a_in[2] = 8;
        b_in[0] = 8; b_in[1] = 5; b_in[2] = 2;
        @(posedge clk);

        a_in[0] = 3; a_in[1] = 6; a_in[2] = 9;
        b_in[0] = 7; b_in[1] = 4; b_in[2] = 1;
        @(posedge clk);

        valid_in = 0;

        // let the array drain; the PE handshake will control flow
        repeat (20) @(posedge clk);

        $display("valid_out=%0d", valid_out);
        for (int i = 0; i < DIM; i++) begin
            for (int j = 0; j < DIM; j++) begin
                $display("c_out[%0d][%0d]=%0d", i, j, c_out[i][j]);
            end
        end

        $finish;
    end

endmodule
