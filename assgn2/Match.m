tic;
imgName1 = argv(){1};
imgName2 = argv(){2};

ratioThreshhold = 0.3;

desc1.name = ['Descriptor_' imgName1 '.desc'];
desc2.name = ['Descriptor_' imgName2 '.desc'];

desc1.IPs = load('-binary', desc1.name).P;
desc2.IPs = load('-binary', desc2.name).P;

desc1.IPcount = size(desc1.IPs.data)(1);
desc2.IPcount = size(desc2.IPs.data)(1);

discardCount = 0;

% Function to get SSD score
function [score] = getMatchingScore(item1, item2)
    score = norm(item1 - item2);
end
% for each pair of IPs, match
for index1 = 1 : desc1.IPcount
    item1 = desc1.IPs.data(index1, :);
    bestMatch(index1).score      = inf;
    bestMatch(index1).itemIndex  = 0;
    best2Match(index1).score     = inf;
    best2Match(index1).itemIndex = 0;

    for index2 = 1 : desc2.IPcount
        item2 = desc2.IPs.data(index2, :);
        score = getMatchingScore(item1, item2);
        if (score < bestMatch(index1).score)
            best2Match(index1).score     = bestMatch(index1).score;
            best2Match(index1).itemIndex = bestMatch(index1).itemIndex;
            bestMatch(index1).score      = score;
            bestMatch(index1).itemIndex  = index2;
        end
    end
    % discard high ratio matches
    if ((bestMatch(index1).score / best2Match(index1).score) > ratioThreshhold )
        bestMatch(index1).score    = inf;
        bestMatch(index1).itemIndex = 0;
        discardCount += 1; % TODO remove this
    end
end
M = [];
i = 0;
for index1 = 1 : desc1.IPcount
    index2 = bestMatch(index1).itemIndex;
    if (index2 != 0)
        M = [M; [desc1.IPs.point(index1, :) desc2.IPs.point(index2, :)]];
    end
end
save('-ascii', ['Match_' imgName1 imgName2 '.match'], 'M')
toc;
sleep(1);
system(['python markMatches.py ' imgName1 ' ' imgName2]);
