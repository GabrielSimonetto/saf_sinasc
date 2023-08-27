def generate_table_header():
    header = """
    \\begin{longtable}{llp{10cm}}
        \caption{Dicionário de Variáveis}
        \label{tab:dicionario_de_variaveis} \\
        \hline
        \\textbf{Coluna} & \\textbf{Tipo} & \\textbf{Descrição} \\
        \hline
        \endfirsthead    
"""
    return header


def generate_table_closing():
    closing = """
        \end{longtable}
        
        \medskip
        \\noindent Tabela adaptada do dado original. Informações adicionais sobre as colunas podem ser encontradas em \cite{fiocruz_table}.
        
        \medskip
        \\noindent \\textbf{Referência:} Tabela da Fiocruz com informações referentes às colunas presentes no dado original.

"""
    return closing


def generate_tex_table(column_names, tex_table):
    table_content = generate_table_header()

    for column_name in column_names:
        column_found = False
        for line in tex_table:
            if column_name in line:
                table_content += "\t\t" + line.strip() + "\n"
                # table_content += line
                column_found = True
                break

        if not column_found:
            table_content += "\t\t" + column_name + " & & \\\\\n"

    table_content += generate_table_closing()

    return table_content


def read_table_descriptions(file_path):
    tex_table = []
    with open(file_path, 'r') as file:
        for line in file:
            tex_table.append(line.strip())
    return tex_table


# Retirei printando dps de feature_engineering
cols_finais = ['CODESTAB', 'CODMUNNASC', 'LOCNASC', 'IDADEMAE', 'ESTCIVMAE', 'ESCMAE',
               'CODOCUPMAE', 'QTDFILVIVO', 'QTDFILMORT', 'CODMUNRES', 'GESTACAO',
               'GRAVIDEZ', 'PARTO', 'CONSULTAS', 'SEXO', 'APGAR1', 'APGAR5', 'RACACOR',
               'PESO', 'CODMUNNATU', 'SERIESCMAE', 'RACACORMAE', 'QTDGESTANT',
               'QTDPARTNOR', 'QTDPARTCES', 'IDADEPAI', 'SEMAGESTAC', 'TPMETESTIM',
               'CONSPRENAT', 'MESPRENAT', 'TPAPRESENT', 'STTRABPART', 'STCESPARTO',
               'TPROBSON', 'STDNEPIDEM', 'STDNNOVA', 'ANO', 'ESCMAE2010', 'CODUFNATU',
               'TPNASCASSI', 'TPFUNCRESP', 'TPDOCRESP', 'ESCMAEAGR1', 'CODMUNCART',
               'ESTADO', 'y', 'is_equal_CODMUNRES_and_CODMUNNASC',
               'is_equal_CODMUNRES_and_CODMUNNATU',
               'is_equal_CODMUNNASC_and_CODMUNNATU', 'is_missing_IDADEPAI']

# contents in latextcc2/chapters/5.1_dicionario_de_variaveis.tex
tex_table_file = "create_report_of_final_columns_input.tex"
tex_table = read_table_descriptions(tex_table_file)

generated_table = generate_tex_table(cols_finais, tex_table)

with open("create_report_of_final_columns_output.txt", 'w') as f:
    f.write(generated_table)

# remember to run this repassing to create_report_of_final_columns_output_permanent.txt
# when needed
print(generated_table)
