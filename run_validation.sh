for (( i=5; i<=90; i+=5 ))
do
    echo "r15_net_g_${i}000"
    echo "JRES_mix_15_valid_LRSR_r15_${i}k"
#    python read.py "file_"$c > "out_"$c
    python inference_realesrgan_copy.py -n r15_net_g_${i}000 -i inputs/JRES_mix_15_valid_LR_r10 -o results/r15/JRES_mix_15_valid_LRSR_r15_${i}k -s 2 --fp32
done

