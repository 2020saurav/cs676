% PART - 3: Matching
tic;

imgName1 = 'img1.png';
imgName2 = 'img3.png';

ratioThreshhold = 0.9;

desc1.name = ['Descriptor_' imgName1 '.mat'];
desc2.name = ['Descriptor_' imgName2 '.mat'];

P1 = load(desc1.name);
P2 = load(desc2.name);
desc1.IPs = P1.P;
desc2.IPs = P2.P;

desc1.IPcount = size(desc1.IPs.data, 1);
desc2.IPcount = size(desc2.IPs.data, 1);

bestScore  = zeros(desc1.IPcount, 1);
bestIndex  = zeros(desc1.IPcount, 1);
best2Score = zeros(desc1.IPcount, 1);
best2Index = zeros(desc1.IPcount, 1);

M = [];
% for each pair of IPs, match
for index1 = 1 : desc1.IPcount
    item1 = desc1.IPs.data(index1, :);
    bestScore(index1) = inf;
    bestIndex(index1) = 0;
    best2Score(index1) = inf;
    best2Index(index1) = 0;

    for index2 = 1 : desc2.IPcount
        item2 = desc2.IPs.data(index2, :);
        score = getMatchingScore(item1, item2);
        if (score < bestScore(index1)) % update bestMatch and best2Match
            best2Score(index1)    = bestScore(index1);
            best2Index(index1)    = bestIndex(index1);
            bestScore(index1)     = score;
            bestIndex(index1)     = index2;
        end
    end
    % discard high ratio matches
    if (bestScore(index1)/best2Score(index1) < ratioThreshhold)
          M = [M; [desc1.IPs.point(index1, :) desc2.IPs.point(bestIndex(index1), :)]];
    end
end
save(['Match_' imgName1 imgName2 '.match'], 'M', '-ascii');
toc;
system(['python markMatches.py ' imgName1 ' ' imgName2]);
