for box = -2:3
    
    for rbfsigma = -2:3
        curr_box = 10^box;
        disp(curr_box);
        curr_sigma = 10^rbfsigma;
        disp(curr_sigma);
        try
            [test, testlab, ttcleaved, to, ts, train, trainlab, a, f, X, Y, T, AUC1, AUCav1, Std, Performanceav,Stdp]  = coduh_latest(WTnextseqstructseqbinary, WTnextseqlabels, 7472 , 14702, curr_box, curr_sigma);
            disp(Std)
            disp(AUCav1)
        catch ME
            warning(ME.message);
        end
    end
end


