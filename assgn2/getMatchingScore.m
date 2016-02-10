% Function to get SSD score
function [score] = getMatchingScore(item1, item2)
    score = norm(item1 - item2);
end