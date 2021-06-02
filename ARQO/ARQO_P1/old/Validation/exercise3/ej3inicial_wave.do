onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -radix hexadecimal /micromipstb/uut/Clk
add wave -noupdate -radix hexadecimal /micromipstb/uut/NRst
add wave -noupdate -radix hexadecimal /micromipstb/uut/MemProgAddr
add wave -noupdate -radix hexadecimal /micromipstb/uut/MemProgData
add wave -noupdate -radix hexadecimal /micromipstb/uut/MemDataAddr
add wave -noupdate -radix hexadecimal /micromipstb/uut/MemDataDataRead
add wave -noupdate -radix hexadecimal /micromipstb/uut/MemDataDataWrite
add wave -noupdate -radix hexadecimal /micromipstb/uut/MemDataWE
add wave -radix hexadecimal -expand [find instances -bydu RegsMIPS -nodu]/regs
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {0 ns} 0}
quietly wave cursor active 0
configure wave -namecolwidth 226
configure wave -valuecolwidth 68
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {0 ns} {3186 ns}
