% Function to calculate f-value using Hessian matrix
function f = Harris(x, y)
    global height width w Gx Gy;
    count = 0;
    H     = zeros(1,3);
    % averaging over a window centered at x,y
    for i = max(x-w/2, 1) : min(x+w/2, width)
        for j = max(y-w/2, 1) : min(y+w/2, height)
            count = count + 1;
            Ix    = Gx(i,j);
            Iy    = Gy(i,j);
            H_new = [Ix^2 Ix*Iy Iy^2];
            H     = H + H_new;
        end
    end
    H     = H / count;
    det   = H(1)*H(3) - H(2)*H(2);
    trace = H(1) + H(3);
    f     = det / trace;
end