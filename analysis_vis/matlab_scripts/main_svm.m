function [labels, distances]  = main_svm(svmrbf, test_data)
 
    try
        labels = svmclassify(svmrbf, test_data);

        shift = svmrbf.ScaleData.shift;
        scale = svmrbf.ScaleData.scaleFactor;
        sv = svmrbf.SupportVectors;
        alphaHat = svmrbf.Alpha;
        bias = svmrbf.Bias;
        kfun = svmrbf.KernelFunction;
        kfunargs = svmrbf.KernelFunctionArgs;
        test_scaled = ( test_data + shift ) .* scale;

        distances = kfun(sv,test_scaled,kfunargs{:})'*alphaHat(:) + bias;
    catch ME
        warning(ME.message);
    end  

                                   
end
