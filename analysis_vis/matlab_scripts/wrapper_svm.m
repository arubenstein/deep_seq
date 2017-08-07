train_name = '/Users/arubenstein//git_repos/deep_seq/analysis_vis/stringent_shiryaev/cleaved_uncleaved_structseq_binary.csv';
formatSpec = '%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%f32,%*s';
formatSpecString = '%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%*f32,%s';
train_file = fopen(train_name);
train_data_raw = textscan(train_file, formatSpec);
fclose(train_file);

train_file = fopen(train_name);
train_labels_raw = textscan(train_file, formatSpecString);

train_labels = train_labels_raw{1,1};
train_data = cell2mat(train_data_raw);

for box = -2:3
    
    for rbfsigma = -2:3
        curr_box = 10^box;
        disp(curr_box);
        curr_sigma = 10^rbfsigma;
        disp(curr_sigma);
        try
            [test, testlab, ttcleaved, to, ts, train, trainlab, a, f, X, Y, T, AUC1, AUCav1, Std, Performanceav,Stdp]  = coduh_latest(train_data, train_labels, sum(ismember(train_labels, 'CLEAVED')), sum(ismember(train_labels, 'UNCLEAVED')), curr_box, curr_sigma);
            disp(Std)
            disp(AUCav1)
        catch ME
            warning(ME.message);
        end
    end
end


