%yoyoyo
%A = Together_Furin; % change to name of matrix
 
 
function [test, testlab, ttcleaved, to, ts, train, trainlab, a, f, X, Y, T, AUC, AUCav, Std, Performanceav,Stdp, atrain, ftrain, Xtrain, Ytrain, Ttrain, AUCtrain, AUCtrainav, Stdtrain, Performancetrainav, Stdptrain]  = coduh(Features, LABELS, n_cleaved, n_uncleaved, boxconstraint, rbfsigma)
%function [test, testlab, ttcleaved, to, ts, train, trainlab, a] = coduh(A, LABELS, cleaved, uncleaved, boxconstraint, rbfsigma)
 
clear test testlab ttcleaved to ts train trainlab a f X Y T AUC AUCav Std Performanceav Stdp atrain ftrain Xtrain Ytrain Ttrain AUCtrain AUCtrainav Stdtrain Performancetrainav Stdptrain
 
 
% A = Together_Furin; % change to name of matrix
[numberofelements len] = size(Features);
% len = 13; %width of matrix
tic
 
%X = [];
%Y = [];
%T = [];
%AUC = [];
 
for s = 1:100
    
    zcleaved = ceil(0.8*n_cleaved);                 %creating10%ofnumelements %ceilroundsoff
    zuncleaved = ceil(0.8*n_uncleaved);
    ttcleaved = randperm(n_cleaved,zcleaved);               %generatingRandomFromNumLength
    ttuncleaved = randperm((numberofelements - n_cleaved), zuncleaved) + n_cleaved;
    t = vertcat(ttcleaved',ttuncleaved');
    to(:,s) = vertcat(ttcleaved',ttuncleaved');
    ts(s) = length(t);
    z = zcleaved + zuncleaved;
    
                                                          %t=sort(t); %sort mat karo
    test(:,:,s) = Features(t,:);
                                                          % testun = A(tuncleaved,:);
                                                          % testc(:,:,s) = vertcat(test, testun);
 
    testlab(:,:,s) = LABELS(t,:);
                                                          % testlabun = LABELS(tuncleaved,:);
                                                          % testlabc(:,:,s) = LABELS(testlab, testlabun);
    
    x = numberofelements - z;
    train(:,:,s) = zeros(x, len);
    trainlab(:,:,s)= cell(x,1);
    clear n1;
    n1 = 1;
    
    for i = 1:numberofelements
        
        if i ~= t(:)
            train(n1,:,s) = Features(i,:);
            trainlab(n1,s) = LABELS(i);
            n1 = n1 + 1;
        end
        
    end
    
    
                                    %  test = HCV_Structure(n,:);
                                    % train = HCV_Structure;
                                    %  train(n,:) = [];
                                    %  y = Labels;
                                    % y(n) = [];
                                    %
    svmrbf =[];
    %options=optimset('maxiter', 50000);
    
    svmrbf=svmtrain(train(:,:,s), trainlab(:,s), 'kernel_function', 'rbf', 'boxconstraint', boxconstraint, 'rbf_sigma', rbfsigma);
    %svmrbf=svmtrain(train(:,:,s), trainlab(:,s));
 
%%TEST%%    
    V = svmclassify(svmrbf,test(:,:,s));
    result = transpose(V);
    a(:,s)=transpose(result);
 
    shift = svmrbf.ScaleData.shift;
                        %fprintf('Calculated shift\n'); 
    scale = svmrbf.ScaleData.scaleFactor;
        %fprintf('Scale!\n'); 
    Xnew = bsxfun(@plus,test(:,:,s),shift);
         %fprintf('Xnew done\n'); 
    Xnew = bsxfun(@times,Xnew,scale);
         %fprintf('Second Xnew done\n'); 
    sv = svmrbf.SupportVectors; 
         %fprintf('SupportVectors done\n'); 
    alphaHat = svmrbf.Alpha;    
          %fprintf('Alpha done\n'); 
    bias = svmrbf.Bias;
         %fprintf('Happy Bias\n');
    kfun = svmrbf.KernelFunction;
         %fprintf('Happy Kfun\n'); 
    kfunargs = svmrbf.KernelFunctionArgs;
          %fprintf('Happy Kfunargs\n');    
    f(:,s) = kfun(sv,Xnew,kfunargs{:})'*alphaHat(:) + bias;
           %fprintf('f calculated yo\n');
           %display(f(:,s));
    %[X(:,s),Y(:,s),T(:,s),AUC(s)]= perfcurve(testlab(:,:,s),f(:,s),'CLEAVED');
    [X,Y,T,AUC(s)]= perfcurve(testlab(:,:,s),f(:,s),'CLEAVED');
    
    AUCav = mean(AUC);
    Std = std(AUC); 
    
%ACCURACY   
    
   tf(:,s) = strcmp (a(:,s), testlab(:,s));
   Performance(s) = sum(tf(:,s)) / numel(a(:,s));
   Performanceav = mean(Performance);
   Stdp = std(Performance);
    
%TRAIN    
    Vtrain = svmclassify(svmrbf,train(:,:,s));
    resulttrain = transpose(Vtrain);
    %clear train
    %end
    atrain(:,s)=transpose(resulttrain);
    
    
    shift = svmrbf.ScaleData.shift;
                        %fprintf('Calculated shift\n'); 
    scale = svmrbf.ScaleData.scaleFactor;
        %fprintf('Scale!\n'); 
    Xnew1 = bsxfun(@plus,train(:,:,s),shift);
         %fprintf('Xnew done\n'); 
    Xnew1 = bsxfun(@times,Xnew1,scale);
         %fprintf('Second Xnew done\n'); 
    sv = svmrbf.SupportVectors; 
         %fprintf('SupportVectors done\n'); 
    alphaHat = svmrbf.Alpha;    
          %fprintf('Alpha done\n'); 
    bias = svmrbf.Bias;
         %fprintf('Happy Bias\n');
    kfun = svmrbf.KernelFunction;
         %fprintf('Happy Kfun\n'); 
    kfunargs = svmrbf.KernelFunctionArgs;
          %fprintf('Happy Kfunargs\n');    
    ftrain(:,s) = kfun(sv,Xnew1,kfunargs{:})'*alphaHat(:) + bias;
           %fprintf('f calculated yo\n');
           %display(f(:,s));
    [g1,g2,g3,g4]= perfcurve(trainlab(:,:,s),ftrain(:,s),'CLEAVED');

    [Xtrain,Ytrain,Ttrain,AUCtrain(s)]= perfcurve(trainlab(:,:,s),ftrain(:,s),'CLEAVED');
    
    AUCtrainav = mean(AUCtrain);
    Stdtrain = std(AUCtrain);
    
   tftrain(:,s) = strcmp (atrain(:,s), trainlab(:,s));
   Performancetrain (s)= sum(tftrain(:,s)) / numel(atrain(:,s));
   Performancetrainav = mean(Performancetrain); 
   Stdptrain = std(Performancetrain);
                                   
end
toc