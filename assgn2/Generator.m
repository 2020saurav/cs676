pkg load image
tic;
imageName = argv(){1};

global patchSize = 16;
global w         = 6; % window-size

img = imread(imageName);
G   = rgb2gray(img);
s   = size(G);

global width  = s(1);
global height = s(2);
global I      = zeros(width, height); % to store image in int matrix
global F      = zeros(width, height); % to store f-values of the image

% G is matrix of uints, I is of ints
for i = 1 : width
    for j = 1 : height
        I(i, j) = G(i, j);
    end
end

% Function to calculate Ix, Iy and formulate the hessian matrix
function H = Hessian(x, y)
    global height width w;
    count = 0;
    H     = zeros(2, 2);
    % averaging over a window centered at x,y
    for i = max(x-w/2, 1) : min(x+w/2, width)
        for j = max(y-w/2, 1) : min(y+w/2, height)
            count   += 1;
            [Ix, Iy] = Grad(i, j);
            H_new    = [Ix^2 Ix*Iy; Ix*Iy Iy^2];
            H        = H + H_new;
        end
    end
    H = H/count;
end

% Function to calculate gradient at the point (i, j)
function [Ix, Iy] = Grad(i, j)
    global height width I;
    if (i == 1)
        Ix = (I(i+1, j) - I(i, j));
    end
    if (j == 1)
        Iy = (I(i, j+1) - I(i, j));
    end
    if (i == width)
        Ix = (I(i, j) - I(i-1, j));
    end
    if (j == height)
        Iy = (I(i, j) - I(i, j-1));
    end
    if (i<width && i>1)
        Ix = (I(i+1, j) - I(i-1, j))/2;
    end
    if (j<height && j>1)
        Iy = (I(i, j+1) - I(i, j-1))/2;
    end
end

% Function to calculate the value of harris operator
function f = Harris(H)
    det   = H(1, 1) * H(2, 2) - H(1, 2) * H(2, 1);
    trace = H(1, 1) + H(2, 2);
    f     = det / trace;
end

% Function to calculate SIFT descriptor for interest point at (x, y) pixel
function M = Sift(x, y)
    global I patchSize height width;
    M = [];
    i1 = max(floor(x-patchSize/2), 1);
    i2 = min(ceil (x+patchSize/2), width);
    j1 = max(floor(y-patchSize/2), 1);
    j2 = min(ceil (y+patchSize/2), height);

    subPatchWidth  = floor(((i2-i1)/4));
    subPatchHeight = floor(((j2-j1)/4));
    h = zeros(16, 1);
    for i = i1 : subPatchWidth : i1 + 3*subPatchWidth
        for j = j1 : subPatchHeight : j1 + 3*subPatchHeight
            %inside a subpatch
            h = zeros(16, 1); % histogram
            for k = i : (i+subPatchWidth)
                for l = j : (j+subPatchHeight)
                    % accessing a pixel, and getting bucket in 0-2pi
                    [Ix, Iy] = Grad(k, l);
                    g = atan2(Iy, Ix);
                    if (g < 0)
                      g += 2*pi;
                    end
                    index = floor((8/pi)*g) + 1;
                    if (index > 16)
                      index = 16;
                    end
                    h(index) = h(index) + 1;
                end
            end
            M = [M; h];
        end
    end
end

% PART - 1 : Harris Corner Detection
% Compute f-value (Harris Detector) for the image
for i = 1 : width
    for j = 1 : height
        H       = Hessian (i, j);
        F(i, j) = Harris(H);
    end
end
imwrite(F, ['Harris_' imageName]);

% PART - 2 : Point Descriptor
% Discretization by threshold (above/below mean)
D = zeros(width, height); % Discrete matrix
T = mean2(F);
for i = 1 : width
    for j = 1:height
        if F(i, j) > T
            D(i, j) = 1;
        end
    end
end
imwrite(D, ['Discrete_' imageName]);

% Find local maxima
IP = false(width, height); % Interest points boolean matrix
for i = 1 : width
    i1 = max(1, i-1);
    i2 = min(width, i+1);
    for j = 1 : height
        j1 = max(1, j-1);
        j2 = min(height, j+1);
        if (D(i, j) >= D(i1, j) && D(i, j) >= D(i, j1)
            && D(i, j) >= D(i1, j1) && D(i, j) >= D(i2, j)
            && D(i, j) >= D(i, j2)  && D(i, j) >= D(i2, j2))
            IP(i, j)   = true;
            IP(i1, j)  = false;
            IP(i, j1)  = false;
            IP(i1, j1) = false;
            IP(i, j2)  = false;
            IP(i2, j)  = false;
            IP(i2, j2) = false;
        end
    end
end
imwrite(IP, ['Interest_' imageName]);

% Descriptor
numPatches = 0;
for i = 1 : width
    for j = 1 : height
        if IP(i, j)
           numPatches += 1;
        end
    end
end

P.data  = zeros(numPatches, 256); % Patches
P.point = repmat([0 0], numPatches, 1);
patchCount = 0;

for i = 1 : width
    for j=1 : height
        if IP(i, j)
          patchCount += 1;
          x = Sift(i, j, patchSize);
          if (size(x)(1)==256)
            P.data(patchCount, :)  = x;
            P.point(patchCount, :) = [i j];
          else
            size(x) % TODO remove this. Ensure it never happens
          end
        end
    end
end
save('-binary', ['Descriptor_' imageName '.desc'], 'P');
toc;
