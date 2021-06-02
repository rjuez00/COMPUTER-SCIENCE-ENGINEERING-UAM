delete wave *
onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -format Logic /micromipsvectorestb/nrst
add wave -noupdate -format Logic /micromipsvectorestb/clk
add wave -noupdate -format Logic /micromipsvectorestb/finsimu
add wave -noupdate -format Literal -radix hexadecimal /micromipsvectorestb/memprogaddr
add wave -noupdate -format Literal -radix hexadecimal /micromipsvectorestb/memdataaddr
add wave -noupdate -format Literal -radix hexadecimal /micromipsvectorestb/memprogdata
add wave -noupdate -format Literal -radix hexadecimal /micromipsvectorestb/memdatadataread
add wave -noupdate -format Literal -radix hexadecimal /micromipsvectorestb/memdatadatawrite
add wave -noupdate -format Logic /micromipsvectorestb/memdatawe
add wave -noupdate -expand -group N -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2048)
add wave -noupdate -expand -group VectorA -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2049)
add wave -noupdate -expand -group VectorA -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2050)
add wave -noupdate -expand -group VectorA -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2051)
add wave -noupdate -expand -group VectorA -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2052)
add wave -noupdate -expand -group VectorA -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2053)
add wave -noupdate -expand -group VectorA -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2054)
add wave -noupdate -expand -group VectorB -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2055)
add wave -noupdate -expand -group VectorB -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2056)
add wave -noupdate -expand -group VectorB -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2057)
add wave -noupdate -expand -group VectorB -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2058)
add wave -noupdate -expand -group VectorB -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2059)
add wave -noupdate -expand -group VectorB -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2060)
add wave -noupdate -expand -group VectorC -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2061)
add wave -noupdate -expand -group VectorC -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2062)
add wave -noupdate -expand -group VectorC -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2063)
add wave -noupdate -expand -group VectorC -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2064)
add wave -noupdate -expand -group VectorC -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2065)
add wave -noupdate -expand -group VectorC -format Literal -radix decimal /micromipsvectorestb/mdata/memdata(2066)
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {133354 ps} 0}
configure wave -namecolwidth 268
configure wave -valuecolwidth 100
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
configure wave -timelineunits us
update
WaveRestoreZoom {0 ps} {1947226 ps}
