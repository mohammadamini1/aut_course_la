import math

p = ''

def show_menu_get_choice():
    r = input("\n--------------\nSelect option:\n\n1) Calculate row echelon matrix\n2) Calculate rank(A) & dim(nul(A))\n3) Exit\nor use \"set p\"\n\n>>> ")
    return r

def open_files():
    z = "zarayeb" + p + ".txt"
    s = "sabet" + p + ".txt"
    
    try:
        zarayeb = open(z)
    except:
        print("\nERORR: zarayeb" + p + ".txt vojod nadarad")
        return "BAD_ZARAYEB_FILE"
        
    try:
        sabet = open(s)
    except:
        print("\nERORR: sabet" + p + ".txt vojod nadarad")
        zarayeb.close()
        return "BAD_SABET_FILE"

    matrix = []

    row = -1
    for i in zarayeb.readlines():
        if i != '\n':
            m = []
            s = i.split()
            this_row = s.__len__()
            if this_row != row and row != -1:
                print("\nERORR: Bad input in zarayeb" + p + ".txt\nin line:\n" + i + "check row integrity\n")
                return "BAD_ZARAYEB_FILE"
            row = this_row

            for j in s:
                m.append(int(j))
            matrix.append(m)

    r = matrix.__len__()
    jj = 0
    for i in sabet.readlines():
        if i != '\n':
            if jj == r:
                print("\nERORR: Bad input in sabet" + p + ".txt\nmore line than expected!\ncheck column integrity\n")
                return "BAD_SABET_FILE"
            if i.split().__len__() > 1:
                print("\nERORR: Bad input in sabet" + p + ".txt\nin column " + str(jj + 1) + "\ncheck column integrity\n")
                return "BAD_SABET_FILE"
            matrix[jj].append(int(i))
            jj = jj + 1

    if jj != r:
        print("\nERORR: Bad input in sabet" + p + ".txt\nless line than expected!\ncheck column integrity\n")
        return "BAD_SABET_FILE"

    zarayeb.close()
    sabet.close()

    return matrix

def show_matrix(m):
    end = '|'
    for i in m:
        for j in i:
            if j < 0:
                print('-', end = '')
            else:
                print(' ', end = '')

            j = j.__abs__()

            if j < 10:
                print(j ,end = ' ' + end)
            else:
                print(j, end = end)
        print()

def have_non_zero(matrix, row, column):
    for i in range(row, matrix.__len__()):
        if matrix[i][column] != 0:
            return True
    return False        

def check_row_is_firstrow(matrix, row, column):
    first_row = row
    for i in range(row, matrix.__len__()):
        if matrix[i][column] != 0:
            first_row = i
            break
    
    log = []
    if first_row != row:
        t = matrix[row]
        matrix[row] = matrix[first_row]
        matrix[first_row] = t
        log.append("row %i and %i switched" % (first_row + 1, row + 1))

    return matrix, log

def satri_pelekali(matrix, row, column):
    matrix, log = check_row_is_firstrow(matrix, row, column)
    taghrib = 3

    # radif haye balatar
    for i in range(0, row):
        m = matrix[i][column] / matrix[row][column] * -1.0
        matrix[i][column] = 0
        for j in range(column + 1, matrix[i].__len__()):
            matrix[i][j] = round(matrix[i][j] + m * matrix[row][j], taghrib)
        if m != 0.0:
            log.append("R" + str(i + 1) + " <- R" + str(i + 1) + " + R" + str(row + 1) + " * " + str(m))

    # radif haye paeen tar
    for i in range(row + 1, matrix.__len__()):
        m = matrix[i][column] / matrix[row][column] * -1.0
        matrix[i][column] = 0
        for j in range(column + 1, matrix[i].__len__()):
            matrix[i][j] = round(matrix[i][j] + m * matrix[row][j], taghrib)
        if m != 0.0:
            log.append("R" + str(i + 1) + " <- R" + str(i + 1) + " + R" + str(row + 1) + " * " + str(m))

    return log

def clean_zero_raws(matrix):
    m = []
    for row in matrix:
        for col in row:
            if col != 0:
                m.append(row)
                break
    return m    

def cal_simpled_equations(matrix):
    ans_file = open("ans" + p + ".txt", 'w')
    
    # if Inconsistent bod:
    for row in reversed(matrix):
        all_zero = True
        if row[row.__len__() - 1] != 0:
            for i in range(0, row.__len__() - 1):
                if row[i] != 0:
                    all_zero = False
                    break
            if all_zero:
                print("Inconsistent!")
                ans_file.write("Inconsistent!")
                ans_file.close()
                return

    print("chon tedade moadelat kamtar az moteghayer hasat => faghat mitavan moadelat ra sade tar kard!")
    ans_file.write("INFINIT_ANSWER\n--------------\n")

    last_row = -1
    for col in range(0, matrix[0].__len__() - 1):
        whole_col_is_zero = True
        for row in range(matrix.__len__() -1, last_row, -1):
            if matrix[row][col] != 0:
                last_row = row
                whole_col_is_zero = False
                print("X%i = %.1f" % (col + 1, matrix[row][-1]), end = '')
                ans_file.write("X%i = %.1f" % (col + 1, matrix[row][-1]))
                for i in range(col + 1, matrix[row].__len__() - 1):
                    if matrix[row][i] != 0:
                        print(" + %.1f*X%i" % (float(matrix[row][i]) * -1.0, i + 1), end = '')
                        ans_file.write(" + %.1f*X%i" % (float(matrix[row][i]) * -1.0, i + 1))
                print()
                ans_file.write('\n')
                break

        if whole_col_is_zero:
            print("X%i = Anything!" % (col + 1))
            ans_file.write("X%i = Anything!" % (col + 1))
            if col != matrix[0].__len__() - 1:
                ans_file.write('\n')

    ans_file.close()

def cal_answer(matrix):
    ans = []
    for row in reversed(range(0, matrix.__len__())):
        all_zero = True
        for col in range(0, matrix[row].__len__() - 1):
            if matrix[row][col] != 0:
                ans.append([col, matrix[row][matrix[row].__len__() - 1]])
                all_zero = False
                break
        if all_zero:
            return "Inconsistent"

    ans.reverse()
    return ans

def show_final_answer(matrix, answer_list):
    ans_file = open("ans" + p + ".txt", 'w')
    if answer_list == "Inconsistent":
        print("Inconsistent!")
        ans_file.write("Inconsistent!")
    else:
        a = -1
        for ans in answer_list:
            print("X%i = %.1f" % (ans[0] + 1, ans[1]))
            ans_file.write("X%i = %.1f" % (ans[0] + 1, ans[1]))
            a = a + 1
            if a != answer_list.__len__() - 1:
                ans_file.write('\n')
    
    ans_file.close()

def create_sabet_file():
    z = open("zarayeb" + p + ".txt")
    row = z.readlines().__len__()
    z.close()

    sabet = open("sabet" + p + ".txt", 'w')
    
    sabet.write("0")
    for i in range(0, row - 1):
        sabet.write("\n0")

    sabet.close()

def have_any_zero_rows(matrix):
    count = 0
    for row in matrix:
        all_zero = True
        for col in row:
            if col != 0:
                all_zero = False
                break
        if all_zero:
            count = count + 1
    return count

def cal_row_echelon(return_final_matrix, matrix):
    if matrix == "BAD_ZARAYEB_FILE" or matrix == "BAD_SABET_FILE":
        return "BAD"

    print("Matris afzode:")
    show_matrix(matrix)

    row = 0
    column = 0
    counter = 0
    while True:
        if have_non_zero(matrix, row, column):
            log = satri_pelekali(matrix, row, column)

            for i in range(column + 1, matrix[0].__len__()):
                matrix[row][i] = round(matrix[row][i] / matrix[row][column], 2)
                if matrix[row][i].__abs__() == 0.0:
                    matrix[row][i] = 0.0
            matrix[row][column] = 1

            counter = counter + 1
            print("\n-------------------------------------------------\nMarhale %i:" % counter)
            for l in log:
                print(l)
            show_matrix(matrix)

            row = row + 1

        column = column + 1

        if row == matrix.__len__() or column == matrix[0].__len__():
            break

    print("\n\nMatrix satri-pelekani nahaei:")
    show_matrix(matrix)
    print()

    matrix = clean_zero_raws(matrix)

    if return_final_matrix:
        return matrix

    if matrix[0].__len__() - 1 > matrix.__len__():
        cal_simpled_equations(matrix)
    else:
        show_final_answer(matrix, cal_answer(matrix))
    print("\nFinal answer saved in ans" + p + ".txt")

def cal_rank_dim(matrix):
    print("\n\n++++++++++++++++++++++\nCalculating Nul(A) ...\n----------------------\n")
    row = 0
    col = 0
    counter = 0

    while True:
        if have_non_zero(matrix, row, col):
            row = row + 1
            counter = counter + 1
            
        col = col + 1
        
        if row == matrix.__len__() or col == matrix[0].__len__() - 1:
            break

    return counter, matrix[0].__len__() - counter - 1

################
################
################

while True:
    choice = show_menu_get_choice()
    if choice == '1':
        print("Matrix Zarayeb ra dar zarayeb" + p + ".txt va Matrix Sabet ra dar sabet" + p + ".txt vared konid")
        print("Countinue? (Enter)", end='')
        input()

        cal_row_echelon(False, open_files())

    elif choice == '2':
        print("Matrix Zarayeb ra dar zarayeb" + p + ".txt vared konid")
        print("Countinue? (Enter)", end='')
        input()

        create_sabet_file()
        m = cal_row_echelon(True, open_files())
        if m != 1:
            rank, dim = cal_rank_dim(m)
            if dim == 0:
                dim = 1
            print("Rank(A) = " + str(rank) + "\ndim(Ax=0) = " + str(dim))

    elif choice == '3':
        quit()
    elif choice == "set p":
        p = input("Enter p: ")
    else:
        print("Bad Input!")
