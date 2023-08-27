# Making a 5x neutral dataset in relation to positive cases

# neutral positive cases between 2010-2019 for each state
# {'AC': 19,
#  'AL': 23,
#  'AM': 37,
#  'AP': 2,
#  'BA': 66,
#  'CE': 51,
#  'DF': 20,
#  'ES': 22,
#  'GO': 47,
#  'MA': 51,
#  'MG': 98,
#  'MS': 10,
#  'MT': 19,
#  'PA': 25,
#  'PB': 30,
#  'PE': 88,
#  'PI': 16,
#  'PR': 65,
#  'RJ': 84,
#  'RN': 27,
#  'RO': 7,
#  'RR': 12,
#  'RS': 51,
#  'SC': 44,
#  'SE': 10,
#  'SP': 330,
#  'TO': 8}

if [ -z "$seed" ]
then
      echo "\$seed is empty, this program expects to be called yielding a value for seed";
      echo "try running something like:";
      echo "export seed=0; ./create_single_sample.sh";
      exit 1;    
fi

states_data="../../data/compilations/by_state";
output_path="../../data/compilations/samples/5x_neutral_entries_$seed.csv"; # TODO: pad 2 zeros to the left

echo "Processing seed: $seed"

# first one creates the file with the header
# all of the other must concat into it with >>
# --random-source=<(yes $seed) fixes the seed 0 making our runs deterministic

# TODO: allow multiplier on stratified constant (19 * 5 instead of 95)
head -n 1  "$states_data/AC_2010_2019.csv"  > "$output_path";
tail -n +2 "$states_data/AC_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 95   >> "$output_path";
tail -n +2 "$states_data/AL_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 115  >> "$output_path";
tail -n +2 "$states_data/AM_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 185  >> "$output_path";
tail -n +2 "$states_data/AP_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 10   >> "$output_path";
tail -n +2 "$states_data/BA_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 330  >> "$output_path";
tail -n +2 "$states_data/CE_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 255  >> "$output_path";
tail -n +2 "$states_data/DF_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 100  >> "$output_path";
tail -n +2 "$states_data/ES_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 110  >> "$output_path";
tail -n +2 "$states_data/GO_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 235  >> "$output_path";
tail -n +2 "$states_data/MA_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 255  >> "$output_path";
tail -n +2 "$states_data/MG_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 490  >> "$output_path";
tail -n +2 "$states_data/MS_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 50   >> "$output_path";
tail -n +2 "$states_data/MT_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 95   >> "$output_path";
tail -n +2 "$states_data/PA_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 125  >> "$output_path";
tail -n +2 "$states_data/PB_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 150  >> "$output_path";
tail -n +2 "$states_data/PE_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 440  >> "$output_path";
tail -n +2 "$states_data/PI_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 80   >> "$output_path";
tail -n +2 "$states_data/PR_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 325  >> "$output_path";
tail -n +2 "$states_data/RJ_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 420  >> "$output_path";
tail -n +2 "$states_data/RN_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 135  >> "$output_path";
tail -n +2 "$states_data/RO_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 35   >> "$output_path";
tail -n +2 "$states_data/RR_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 60   >> "$output_path";
tail -n +2 "$states_data/RS_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 255  >> "$output_path";
tail -n +2 "$states_data/SC_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 220  >> "$output_path";
tail -n +2 "$states_data/SE_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 50   >> "$output_path";
tail -n +2 "$states_data/SP_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 1650 >> "$output_path";
tail -n +2 "$states_data/TO_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 40   >> "$output_path";

echo "Finished creating $output_path";