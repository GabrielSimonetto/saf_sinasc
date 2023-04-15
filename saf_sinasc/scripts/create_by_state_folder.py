from pathlib import Path
import glob
import pandas as pd

# assert False, """I have never ran this script,
#     it's taken directly from a notebook on "tcc/notebooks"
#     (not to be mistaken with tcc/saf_sinasc/notebooks)

#     I don't even know why I am documenting this,
#         if you truly need this just know you are on your own
#         god has abandoned you

#     Test this in a safe place
# """


DRIVE_PATH = Path("data")

SINASC_INITIAL_YEAR = 2010
SINASC_LAST_YEAR = 2019

folder_path = DRIVE_PATH
raw_path = folder_path/"raw"


# assert False, "Extremely professional way to run a script 6 times without breaking kernel on a jupyter notebook"
state_list = [
    #     'PB', 'AL', 'MT', 'AM', 'GO', 'DF', 'RR',
    #     'SP',
    #     'PR', 'TO', 'RS',
    #     'AC', 'SC', 'PA', 'CE', 'MG',
    #     'AP', 'PE', 'PI', 'RN', 'BA', 'ES',
    'MA', 'RJ', 'SE', 'RO', 'MS'
]

for state in state_list:
    output_path = folder_path/"compilations"/"by_state" / \
        f"{state}_{SINASC_INITIAL_YEAR}_{SINASC_LAST_YEAR}.csv"

    files_path = glob.glob(f"{raw_path}/**/SINASC-{state}**.csv")
    # assert(len(files_path) == 10, f"We had a len of {len(files_path)}")
    assert (len(files_path) == 10)

    output = pd.DataFrame()

    for file_path in files_path:
        df = pd.read_csv(file_path)
        year = file_path.split("SINASC-")[1].split("-")[1].split(".")[0]

        drop_cols = [_ for _ in df.columns if (
            'unnamed' in _.lower()) or ('contador' in _.lower())]
        df.drop(columns=drop_cols, axis=1, inplace=True)
        df["ANO"] = year

        output = pd.concat([output, df])
        print(f"Successful append on {file_path}, shape of {df.shape}")

    # overwrite csv
    output["ESTADO"] = state
    output.to_csv(output_path, index=False)
    print(f"Successful final write on {output_path}, shape of {output.shape}")
    print()

    del output
