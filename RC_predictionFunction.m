function RunSegmentation(imagePattern, outputFolder)

    % Load the trained network
    load('RCDetection_v1.mat')

    imgSize = [1024, 1024];

    % Ensure output folder exists
    if ~exist(outputFolder, 'dir')
        mkdir(outputFolder);
    end

    % Get list of images to process
    files = dir(imagePattern);

    for ii = 1:length(files)
        img = imread(fullfile(files(ii).folder, files(ii).name));
        img = StandardizeImage(img, imgSize);

        predictedLabels = semanticseg(img, trainedNet);
        coloredLabels = MapLabels2Colors(predictedLabels);

        % Create a figure but don't show it
        fig = figure('visible', 'off');
        subplot(1, 2, 1)
        imshow(img)
        title('Original Image')

        subplot(1, 2, 2)
        imshow(coloredLabels)
        title('Predicted Mask')

        % Set figure size
        set(gcf, 'position', [1 41 1824 1103]*0.8)

        % Save the figure as a .png file
        [~, baseName, ~] = fileparts(files(ii).name);
        savePath = fullfile(outputFolder, [baseName, '_segmented.png']);
        saveas(fig, savePath);

        close(fig);  % Close the figure to free memory
    end
end

function imgStd = StandardizeImage(img, imgSize)
    imsize = size(img);
    padH = round(max([0, imsize(2)-imsize(1), imgSize(1)-imsize(1)]) / 2);
    padW = round(max([0, imsize(1)-imsize(2), imgSize(2)-imsize(2)]) / 2);
    imgStd = padarray(img, [padH, padW]);
    imgStd = imresize(imgStd, imgSize);
end

function coloredLabels = MapLabels2Colors(predictedLabels)
    damaged = [250, 50, 83];
    undamaged = [51, 221, 255];
    background = [0, 0, 0];
    cmap = [background; undamaged; damaged] / 255;
    labelIDs = uint8(predictedLabels);
    coloredLabels = label2rgb(labelIDs, cmap);
end
