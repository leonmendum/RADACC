def dump_matrix(matrix, file, format_string="{val}"):
    with open("dumps/"+file, 'w') as file:
        for row in matrix:
            for val in row:
                file.write(format_string.format(val) + " ")
            file.write('\n')