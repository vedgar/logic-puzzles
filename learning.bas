

memory[53280:53282] = 13, 6
clear_screen()
cmd = open(device='disk', channel='command', fileno=15)
f1, f2, m = np.zeros(43), np.zeros(43), np.zeros(43, 43)

initialize_screen:
    clear_screen()
    print('    neuron network associative memory')
    print('\n' * 12)
    print('f1 - teach pattern     f2 - dump matrix')
    print('f3 - randomize pattern f4 - forget all ')
    print('f5 - recall pattern    f6 - quit       ')
    print('f7 - disc save         f8 - disc load  ')
    print()
    print('a-z, 0-9: load pattern')
    draw_borders(r1=4, c1=5)
    draw_borders(r1=4, c1=25)
    update_f2_on_screen()
    update_f1_on_screen()

loop:
    status(' ready    ')
    a = get_key()
    status('          ')
    k = asc(a)
    if a.isdigit(): k += 64
    elif not a.islower(): goto dispatch_fn_keys
    status(f'fetch {a}')
    l = 0
    k = (k-64) * 8 + 53248
    memory[56333] = 127
    memory[1] &=~ 4
    memory[49408:49415] = memory[k:k+7]
    memory[1] |= 4
    memory[56333] = 129
    for i in 0, 1, 2, 3, 4, 5, 6:
      j = memory[49408+i] // 2
      for k in 1, 2, 3, 4, 5, 6:
        l += 1
        f1[l] = 1 if j % 2 else -1
        j //= 2
    update_f1_on_screen()
    update_f2_on_screen()
    goto loop

dispatch_fn_keys:
    j = ord(a) - 132
    if j == 1: train_f1_pattern(); goto loop
    if j == 5: print_matrix_part(); goto initialize_screen
    if j == 2: randomize_f1(); goto loop
    if j == 6: forget_all(); goto loop
    if j == 3: pattern_recall(); goto loop
    if j == 7: clear_screen(); cmd.close(); raise SystemExit
    if j == 4: disk_save(); goto initialize_screen
    if j == 8: disk_load(); goto initialize_screen
    go to loop

--- subroutines

def draw_borders(r1, c1):
600 rem draw borders for fields
610 for i=0 to 1
620   v=1024+40*(r1+(i*8))+c1
630   poke v,112+(-3*i)
640   for j=1 to 8
650     poke v+j,67
660   next j
670   poke v+9,110+(15*i)
680 next i
690 for i=1 to 7
700   v=1024+40*(r1+i)+c1
710   poke v,93
720   poke v+9,93
730 next i
740 return

def update_f1_on_screen():
750 rem update field f2% on screen
760 l%=0
770 for i in 0, 1, 2, 3, 4, 5, 6:
780   v = video_address(row=i+5, col=6)
790   for j in 2, 3, 4, 5, 6, 7:
800     l += 1
810     memory[v + 8 - j] = 81 if f1[l] == 1 else 32

def update_f2_on_screen():
860 rem update field f1% on screen
870 l = 0
880 for i in 0, 1, 2, 3, 4, 5, 6:
890   v = video_address(row=i+5, col=26)
900   for j in 2, 3, 4, 5, 6, 7:
910     l += 1
920     memory[v + 8 - j] = 81 if f2[l] == 1 else 32

def status(s):
    clear_screen(False)
    print('\n' * 21)
    print(' ' + s.ljust(8))

def train_f1_pattern():
1010 status('training')
1020 for i = 1 to 42
1030   for j = 1 to 42
1040     m%(i,j)=m%(i,j)+f1%(i)*f1%(j)
1050   next j
1060 next i
1070 return

def print_matrix_part():
1080 rem print part of matrix
1090 print chr$(147);
1100 for i = 1 to 24
1110   for j = 1 to 39
         print(end=chr(150 if m[i, j] < 0 else 154))
1140     print(str(abs(m[i, j])))
1160   print()
1180 print(chr$(154), end='press any key to continue:')
1190 get_key()

def randomize_f1():
1210 rem randomise 10 percent of f1%
1220 status('random')
1230 for i=1 to 42
1240   if random.random() <= 0.1:
1250     f1[i] *= -1
1270 update_f2_on_screen()

def pattern_recall():
1290 rem recall from pattern
1300 status('recall')
1310 p%=1024+40*9+19

1320 rem initially copy f1 to f2
1330 poke p%+1,asc("=")
1340 for i=1 to 42
1350   f2%(i) = f1%(i)
1360 next i
1370 update_f2_on_screen()

def pass_f12():
1380 rem f1 to f2 pass
1390 poke p%,asc("=")
1400 poke p%+2,asc(">")
1410 for j=1 to 42
1420   v%=0
1430   for i=1 to 42
1440     v% = v% + f1%(i) * m%(i,j)
1450   next i
1460   v% = sgn(v%)
1470   if v% <> 0 then f2%(j) = v%
1480 next j
1490 update_f2_on_screen()

def pass_f21():
1500 rem f2 to f1 pass
1510 c%=0
1520 poke p%,asc("<")
1530 poke p%+2,asc("=")
1540 for i=1 to 42
1550   v%=0
1560   for j=1 to 42
1570     v% = v% + f2%(j) * m%(i,j)
1580   next j
1590   v% = sgn(v%)
1600   if v% <> 0 and v% <> f1%(i) then f1%(i) = v% : c% = 1
1610 next i
1620 update_f1_on_screen()
1630 if c% <> 0 goto 1380
1640 poke p%,asc(" ")
1650 poke p%+1,asc(" ")
1660 poke p%+2,asc(" ")
1670 return

def forget_all():
1680 rem forget all - clear memory
1690 status('forget')
1700 for i=1 to 42
1710   f1%(i)=0
1720   f2%(i)=0
1730   for j=1 to 42
1740     m%(i,j)=0
1750   next j
1760 next i
1770 update_f1_on_screen()
1780 update_f2_on_screen()
1790 return

def disk_save():
1800 rem save state to disc file
1810 status('save')
1820 print "";
1830 input "file name: ";a$
1840 a$="@0:"+a$+",s,w"
1850 open 5,8,5,a$
1860 for i=1 to 42:print#5,f1%(i):next
1870 disk_error_check()
1880 for i=1 to 42:print#5,f2%(i):next
1890 disk_error_check()
1900 for i=1 to 42
1910   for j=1 to 42
1920     print#5,m%(i,j)
1930   next j
1940   disk_error_check()
1950 next i
1960 close 5
1970 print "";
1980 return

def disk_load():
1990 rem restore state from disc file
2000 status('restore')
2010 print "";
2020 input "file name: ";a$
2030 a$="@0:"+a$+",s,r"
2040 p%=asc("m")
2050 disk_error_check()
2060 open 5,8,5,a$
2070 for i=1 to 42
2080   input#5,f1%(i)
2090 next i
2100 disk_error_check()
2110 for i=1 to 42
2120   input#5,f2%(i)
2130 next i
2140 disk_error_check()
2150 for i=1 to 42
2160   for j=1 to 42
2170     input#5,m%(i,j)
2180   next j
2190   disk_error_check()
2200 next i
2210 close 5
2220 return

disk_error_check()
2230 rem disc error check
2240 input#15, en, em$, et, es
2250 if en > 0 then print en, em$, et, es : stop
2260 return