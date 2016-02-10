% Function to calculate SIFT descriptor for interest point at (x, y) pixel
function M = Sift(x, y)
    global patchSize height width Gx Gy;
    M = [];
    i1 = max(floor(x-patchSize/2), 1);
    i2 = min(ceil (x+patchSize/2), width);
    j1 = max(floor(y-patchSize/2), 1);
    j2 = min(ceil (y+patchSize/2), height);
    subPatchWidth  = floor(((i2-i1)/4));
    subPatchHeight = floor(((j2-j1)/4));

    theta = atan2(Gy(x,y), Gx(x,y)); % Orientation of the key point
    if (theta < 0)
        theta = theta + 2*pi;
    end

    for i = i1 : subPatchWidth : i1 + 3*subPatchWidth
        for j = j1 : subPatchHeight : j1 + 3*subPatchHeight
            %inside a subpatch
            h = zeros(16, 1); % histogram

            for k = i : (i+subPatchWidth)
                for l = j : (j+subPatchHeight)
                    % accessing a pixel
                    Ix = Gx(k,l);
                    Iy = Gy(k,l);
                    grad = sqrt(Ix*Ix+ Iy*Iy);
                    patchTheta = atan2(Iy, Ix);
                    if (patchTheta < 0)
                      patchTheta = patchTheta + 2*pi;
                    end
                    g = patchTheta - theta; % relative gradient of subpatch
                    if (g < 0)
                        g = g + 2*pi;
                    end
                    index = floor(8*g/pi) + 1; % index of the bin
                    if (index > 16)
                      index = 16;
                    end
                    h(index) = h(index) + grad;

                end
            end
            h = h / norm(h);
            M = [M; h];
        end
    end
end
