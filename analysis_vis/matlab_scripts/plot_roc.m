struct = figure('visible','off');

plot(X_seq_reg_prerec, Y_seq_reg_prerec, X_structseq_reg_prerec, Y_structseq_reg_prerec, 'LineWidth',3);
xlabel('False Positive Rate');
ylabel('True Positive Rate');
set(gca,'fontsize',18);
legend('Previous Expt','Curr Expt','Curr Expt Stringent');
saveas(struct,'/Users/arubenstein/git_repos/deep_seq/analysis_vis/results/roc_shiryaev_curr','jpg');

cleaved_all_over2 = allseqs(distances_seq_all > 2 & strcmp(pred_labels_seq_all,'CLEAVED'));
cleaved_all_under2 = allseqs(distances_seq_all <= 2 & strcmp(pred_labels_seq_all,'CLEAVED'));
uncleaved_all_over2 = allseqs(distances_seq_all > -2 & strcmp(pred_labels_seq_all,'UNCLEAVED'));
uncleaved_all_under2 = allseqs(distances_seq_all <= -2 & strcmp(pred_labels_seq_all,'UNCLEAVED'));
is_cleaved = ismember(cleaved_all,WTnextseqcleaved);
is_uncleaved = ismember(cleaved_all,WTnextsequncleaved);
is_middle = ismember(cleaved_all,WTnextsequncleaved);
status_cl = zeros(numel(cleaved_all),1);
status_uncl = zeros(numel(cleaved_all),1);
status_mid = zeros(numel(cleaved_all),1);

status_cl(is_cleaved) = 3;
status_uncl(is_uncleaved) = 1;
status_mid(is_middle) = 2;

statuses = horzcat(status_cl,status_uncl,status_mid);

status = max(statuses,[],2);

fid=fopen('/Users/arubenstein/git_repos/deep_seq/analysis_vis/stringent_shiryaev/status.txt','wt');
fprintf(fid,'%d\n',status);
fclose(fid);
fid=fopen('/Users/arubenstein/git_repos/deep_seq/analysis_vis/stringent_shiryaev/pred_labels.txt','wt');
fprintf(fid,'%s\n',pred_labels);

for row=1:size(pred_labels,1)
    fprintf(fid,'%s\n',pred_labels{row,:});
end
fclose(fid);