function [coloring] = SudokuRandColoring()
%SUDOKURANDCOLORING Randomly colors a sudoku grid with 9 of each of 9
%colors
%   Detailed explanation goes here
    % this is the first color
    % figure out which ones are color 1
    duplicate = true;
    while duplicate == true
        rand1s = randi(81,[1,9]);
        duplicate = false;
        for k=1:9
            for j=1:9
                if k~=j && rand1s(k)==rand1s(j)
                    duplicate = true;
                end
            end
        end
    end
    
    % do the coloring
    coloring = zeros(1,81);
    for k = 1:9
        coloring(rand1s(k))=1;
    end
    
    % move on to the next color
    duplicate = true;
    while duplicate == true
        rand2s = randi(81,[1,9]);
        duplicate = false;
        for k=1:9
            for j=1:9
                if (k~=j && rand2s(k)==rand2s(j)) || coloring(rand2s(k))~=0
                    duplicate = true;
                end
            end
        end
    end
    
    % do the coloring
    for k = 1:9
        coloring(rand2s(k))=2;
    end
    
    % move on to the next color
    duplicate = true;
    while duplicate == true
        rand3s = randi(81,[1,9]);
        duplicate = false;
        for k=1:9
            for j=1:9
                if (k~=j && rand3s(k)==rand3s(j)) || coloring(rand3s(k))~=0
                    duplicate = true;
                end
            end
        end
    end
    
    % do the coloring
    for k = 1:9
        coloring(rand3s(k))=3;
    end
    
    % move on to the next color
    duplicate = true;
    while duplicate == true
        rand4s = randi(81,[1,9]);
        duplicate = false;
        for k=1:9
            for j=1:9
                if (k~=j && rand4s(k)==rand4s(j)) || coloring(rand4s(k))~=0
                    duplicate = true;
                end
            end
        end
    end
    
    % do the coloring
    for k = 1:9
        coloring(rand4s(k))=4;
    end
    
    % move on to the next color
    duplicate = true;
    while duplicate == true
        rand5s = randi(81,[1,9]);
        duplicate = false;
        for k=1:9
            for j=1:9
                if (k~=j && rand5s(k)==rand5s(j)) || coloring(rand5s(k))~=0
                    duplicate = true;
                end
            end
        end
    end
    
    % do the coloring
    for k = 1:9
        coloring(rand5s(k))=5;
    end
    
    % move on to the next color
    duplicate = true;
    while duplicate == true
        rand6s = randi(81,[1,9]);
        duplicate = false;
        for k=1:9
            for j=1:9
                if (k~=j && rand6s(k)==rand6s(j)) || coloring(rand6s(k))~=0
                    duplicate = true;
                end
            end
        end
    end
    
    % do the coloring
    for k = 1:9
        coloring(rand6s(k))=6;
    end
    
    % move on to the next color
    duplicate = true;
    while duplicate == true
        rand7s = randi(81,[1,9]);
        duplicate = false;
        for k=1:9
            for j=1:9
                if (k~=j && rand7s(k)==rand7s(j)) || coloring(rand7s(k))~=0
                    duplicate = true;
                end
            end
        end
    end
    
    % do the coloring
    for k = 1:9
        coloring(rand7s(k))=7;
    end
    
    % move on to the next color
    duplicate = true;
    while duplicate == true
        rand8s = randi(81,[1,9]);
        duplicate = false;
        for k=1:9
            for j=1:9
                if (k~=j && rand8s(k)==rand8s(j)) || coloring(rand8s(k))~=0
                    duplicate = true;
                end
            end
        end
    end
    
    % do the coloring
    for k = 1:9
        coloring(rand8s(k))=8;
    end
    
    for k=1:81
        if coloring(k)==0
            coloring(k)=9;
        end
    end

end