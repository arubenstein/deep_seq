interval = ceil(size(test_data,1)/100);
disp(interval)
full_results = [];

for i = 0:100
    ind_start = i*interval+1;
    ind_end = (i+1)*interval;
    if ind_end > size(test_data,1)
        curr_test = test_data(ind_start:end,:);
    else
        curr_test = test_data(ind_start:ind_end,:);
    end
    try
        curr_results = main_svm(structseq_binary_norm_11, labels_11, structseq_binary_norm_11, 100, 1000);
        full_results = [full_results; curr_results];
    catch ME
        warning(ME.message);
    end
end


