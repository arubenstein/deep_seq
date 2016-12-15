function [V]  = main_svm(train, trainlab, test, boxconstraint, rbfsigma)
 
%clear test testlab ttcleaved to ts train trainlab a f X Y T AUC AUCav Std Performanceav Stdp atrain ftrain Xtrain Ytrain Ttrain AUCtrain AUCtrainav Stdtrain Performancetrainav Stdptrain
    svmrbf =[];
    
    svmrbf=svmtrain(train, trainlab, 'kernel_function', 'rbf', 'boxconstraint', boxconstraint, 'rbf_sigma', rbfsigma);
 
%%TEST%%    
    V = svmclassify(svmrbf,test);    

                                   
end
