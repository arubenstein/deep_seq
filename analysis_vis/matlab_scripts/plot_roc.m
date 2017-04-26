struct = figure('visible','off');

plot(X_seq_reg_prerec, Y_seq_reg_prerec, X_structseq_reg_prerec, Y_structseq_reg_prerec, 'LineWidth',3);
xlabel('False Positive Rate');
ylabel('True Positive Rate');
set(gca,'fontsize',18);
legend('Previous Expt','Curr Expt','Curr Expt Stringent');
saveas(struct,'/Users/arubenstein/git_repos/deep_seq/analysis_vis/results/roc_shiryaev_curr','jpg');

cleaved_all_over2 = allseqs(distances_seq_011 > 2 & strcmp(pred_labels_seq_011,'CLEAVED'));
cleaved_all_under2 = allseqs(distances_seq_011 <= 2 & strcmp(pred_labels_seq_011,'CLEAVED'));
uncleaved_all_over2 = allseqs(distances_seq_011 > -2 & strcmp(pred_labels_seq_011,'UNCLEAVED'));
uncleaved_all_under2 = allseqs(distances_seq_011 <= -2 & strcmp(pred_labels_seq_011,'UNCLEAVED'));
is_cleaved = ismember(uncleaved_all_under2,cleaved_011);
is_uncleaved = ismember(uncleaved_all_under2,uncleaved_011);
is_middle = ismember(uncleaved_all_under2,middle_011);
sum(is_cleaved)
sum(is_middle)
sum(is_uncleaved)

status_cl = zeros(numel(cleaved_all),1);
status_uncl = zeros(numel(cleaved_all),1);
status_mid = zeros(numel(cleaved_all),1);

status_cl(is_cleaved) = 3;
status_uncl(is_uncleaved) = 1;
status_mid(is_middle) = 2;

statuses = horzcat(status_cl,status_uncl,status_mid);

status = max(statuses,[],2);

fid=fopen('/Users/arubenstein/git_repos/deep_seq/analysis_vis/svm_results/101_sequence_labels.txt','wt');
for row = 1:3200000
    fprintf(fid,'%s\n',pred_labels_seq_101{row,:});
end
fclose(fid);
