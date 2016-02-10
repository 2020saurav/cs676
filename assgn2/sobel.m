tic;

global patchSize w Gx Gy width height I F;

imageName = 'bro2.png';
patchSize = 32;
w         = 6; % window size to average the Hessian matrix

img = imread(imageName);
G   = rgb2gray(img);
s   = size(G);

% Sobel Kernel
Sx = [-1 0 1; -2 0 2; -1 0 1];
Sy = [-1 -2 -1; 0 0 0; 1 2 1];
% Gradient using Sobel Kernel
Gx = conv2(G, Sx, 'same');
Gy = conv2(G, Sy, 'same');

width  = s(1);
height = s(2);
I      = zeros(width, height); % to store image in int matrix
F      = zeros(width, height); % to store f-values of the image

% G is matrix of uints, I is of ints
for i = 1 : width
    for j = 1 : height
        I(i, j) = G(i, j);
    end
end

% PART - 1 : Harris Corner Detection
% Compute f-value (Harris Detector) for the image
for i = 1 : width
    for j = 1 : height
        F(i, j) = Harris(i, j);
    end
end
imwrite(F, ['Harris_' imageName]);

% PART - 2 : Point Descriptor
% 2a. Discretization by threshold (above/below mean)
D = zeros(width, height); % Discrete matrix
T = mean2(F) + sqrt(var(F(:)));
for i = 1 : width
    for j = 1:height
        if F(i, j) > T
            D(i, j) = F(i,j);
        end
    end
end
imwrite(D, ['Discrete_' imageName]);

% 2b. Find local maxima
IP = D > imdilate(D, [1 1 1; 1 0 1; 1 1 1]);
imwrite(IP, ['Interest_' imageName]);

% 2c. Descriptor
numPatches = sum(sum(IP));
P.data     = zeros(numPatches, 256); % Patches
P.point    = repmat([0 0], numPatches, 1);

patchCount = 0;
for i = 1 : width
    for j = 1 : height
        if IP(i, j)
          patchCount             = patchCount + 1;
          P.data(patchCount, :)  = Sift(i, j);
          P.point(patchCount, :) = [i j];
        end
    end
end

save(['Descriptor_' imageName '.mat'], 'P');
toc;
