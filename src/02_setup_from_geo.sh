# bash script to create .yml file 

HOMEPATH="../data"
INPUT="$HOMEPATH/metadata/GSE96611_metadata_short.tsv"
NAME="Stadhouders"
genome="mm9"
genome_upper=$(echo $genome | awk '{print toupper($0)}')
postfix="_$NAME"

echo $genome_upper

# Copy genome and chromosomes sizes
mkdir -p test_${genome}${postfix}/genome
cp ${HOMEPATH}/genomes/${genome}.fa.gz test_${genome}${postfix}/genome
cp ${HOMEPATH}/genomes/${genome}.reduced.chrom.sizes test_${genome}${postfix}/genome

# Index the genome, time-consuming step
cd test_${genome}${postfix}/genome
bwa index ${genome}.fa.gz
cd ../../

# Set output name and start to fill it
param_out=${HOMEPATH}/distiller_yml/"project_${genome}${postfix}.yml"

sep="    "

printf "do_fastqc: False\ndo_stats: True\n\n" > $param_out
printf "input:\n${sep}raw_reads_paths:\n" >> $param_out

list_libraries=()
declare -A dir_libraries

while IFS=$'\t' read -r id author cell_type data gse paper file file2 protocol_short rep series source species stage title treatment running_mode rep_tech
do 
  name=$(basename $file)
  name2=$(basename $file2)

  pref_lib=${cell_type}_${treatment}_${stage}
  pref=${cell_type}_${treatment}_${stage}_${rep}
  file=${file/\/home/$HOMEPATH}
  file2=${file2/\/home/$HOMEPATH}

  if [[ $rep = *"NA"* ]]; then rep='1'; fi
  echo "$id|$author|$cell_type|$data|$gse|$paper|$treatment|$rep|$rep_tech|$pref|$running_mode"
  echo $file $file2 $name $name2 
  echo test_${genome}${postfix}/fastq/${pref}/lane$rep_tech/${name} 

  mkdir -p test_${genome}${postfix}/fastq/${pref}/lane$rep_tech/
  ln -s $file  test_${genome}${postfix}/fastq/${pref}/lane$rep_tech/$name
  ln -s $file2 test_${genome}${postfix}/fastq/${pref}/lane$rep_tech/$name2
  
  if [[ $rep_tech = "1" ]]
  then 
    printf "${sep}${sep}${pref}:\n"  >> $param_out
    if [[ $rep_tech = "1" ]]
    then 
      list_libraries+=($pref_lib)
      dir_libraries[${pref_lib}]+="$pref "
    fi
  fi

  printf "${sep}${sep}${sep}lane$rep_tech:\n"  >> $param_out
  printf "${sep}${sep}${sep}${sep}- test_${genome}${postfix}/fastq/${pref}/lane$rep_tech/${name}\n"  >> $param_out
  printf "${sep}${sep}${sep}${sep}- test_${genome}${postfix}/fastq/${pref}/lane$rep_tech/${name2}\n"  >> $param_out

done < <(tail -n +2 $INPUT | sort -k3,4 -k14,15 -k16,17 -k10,11 -k18,19)

printf "\n\n${sep}library_groups:\n"  >> $param_out

for key in ${!dir_libraries[@]}
do
  echo ${key},${dir_libraries[${key}]}
  printf "${sep}${sep}${key}:\n" >> $param_out

  for i in ${dir_libraries[${key}]}
  do
    printf "${sep}${sep}${sep}- ${i}\n" >> $param_out
  done
done

printf "\n\n${sep}all:\n"  >> $param_out
for key in ${!dir_libraries[@]}
do
  echo ${key},${dir_libraries[${key}]}
  for i in ${dir_libraries[${key}]}
  do
    printf "${sep}${sep}- ${i}\n" >> $param_out
  done
done

printf "${sep}genome:\n"  >> $param_out
printf "${sep}${sep}assembly: \'${genome}\'\n"  >> $param_out
printf "${sep}${sep}bwa_index_wildcard: \'test_${genome}${postfix}/genome/${genome}.*\'\n"  >> $param_out
printf "${sep}${sep}chrom_sizes_path: \'test_${genome}${postfix}/genome/${genome}.reduced.chrom.sizes\'\n"  >> $param_out

tail -n 50 ${HOMEPATH}/distiller_yml/project.yml | sed "s/test/test_${genome}${postfix}/g" >> $param_out
