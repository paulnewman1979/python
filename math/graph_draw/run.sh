python3 main.py \
    --point_num 4 \
    --margin 15 \
    --values \
     "0.p B 0 0,"`
    `"1.p C 200 0,"`
    `"2.a ABC 75,"`
    `"3.a BCA 75,"`
    `"4.a ABD 60,"`
    `"5.a ACD 60" \
    --inductions \
     "0.pp2d BC v0 v1,"`
    `"1.d2d BA i0 v2,"`
    `"2.pd2l lBA v0 i1,"`
    `"3.pp2d CB v1 v0,"`
    `"4.d2d CA i3 v3,"`
    `"5.pd2l lCA v1 i4,"`
    `"6.ll2p A i2 i5,"`
    `"7.d2d BD i1 v4,"`
    `"8.pd2l lBD v0 i7,"`
    `"9.d2d CD i4 v5,"`
    `"10.pd2l lCD v1 i9,"`
    `"11.ll2p D i8 i10,"`
    `"12.pp2m mAB v0 r6,"`
    `"13.lm2p F i7 v0 i12" \
    --lines \
    "AB AC BC AD BD CD" \
    --dot_lines \
    "AF DF CF"

