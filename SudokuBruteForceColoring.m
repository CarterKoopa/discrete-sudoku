clear
close all
clc

%% 
k9 = ones(9);
k9 = k9 - diag(ones(1,9));
allconn = zeros(81);
% this does rows
for k = 1:9
    allconn(9*k-9+1:9*k,9*k-9+1:9*k)=k9;
end
% columns
for k=1:81
    for j=1:81
        if mod(k,9)==mod(j,9) && k~=j
            allconn(j,k)=1;
        end
    end
end
% Boxes
for k=1:81
    for j=1:81
        if (k==1 || k==2 || k==3 || k==10 || k==11 || k==12 || k==19 || k==20 || k==21) && (j==1 || j==2 || j==3 || j==10 || j==11 || j==12 || j==19 || j==20 || j==21) && k~=j
            allconn(j,k)=1;
        elseif (k==7 || k==8 || k==9 || k==16 || k==17 || k==18 || k==25 || k==26 || k==27) && (j==7 || j==8 || j==9 || j==16 || j==17 || j==18 || j==25 || j==26 || j==27) && k~=j
            allconn(j,k)=1;
        elseif (k==4 || k==5 || k==6 || k==13 || k==14 || k==15 || k==22 || k==23 || k==24) && (j==4 || j==5 || j==6 || j==13 || j==14 || j==15 || j==22 || j==23 || j==24) && k~=j
            allconn(j,k)=1;
        elseif (k==28 || k==29 || k==30 || k==37 || k==38 || k==39 || k==46 || k==47 || k==48) && (j==28 || j==29 || j==30 || j==37 || j==38 || j==39 || j==46 || j==47 || j==48) && k~=j
            allconn(j,k)=1;
        elseif (k==31 || k==32 || k==33 || k==40 || k==41 || k==42 || k==49 || k==50 || k==51) && (j==31 || j==32 || j==33 || j==40 || j==41 || j==42 || j==49 || j==50 || j==51) && k~=j
            allconn(j,k)=1;
        elseif (k==34 || k==35 || k==36 || k==43 || k==44 || k==45 || k==52 || k==53 || k==54) && (j==34 || j==35 || j==36 || j==43 || j==44 || j==45 || j==52 || j==53 || j==54) && k~=j
            allconn(j,k)=1;
        elseif (k==55 || k==56 || k==57 || k==64 || k==65 || k==66 || k==73 || k==74 || k==75) && (j==55 || j==56 || j==57 || j==64 || j==65 || j==66 || j==73 || j==74 || j==75) && k~=j
            allconn(j,k)=1;
        elseif (k==58 || k==59 || k==60 || k==67 || k==68 || k==69 || k==76 || k==77 || k==78) && (j==58 || j==59 || j==60 || j==67 || j==68 || j==69 || j==76 || j==77 || j==78) && k~=j
            allconn(j,k)=1;
        elseif (k==61 || k==62 || k==63 || k==70 || k==71 || k==72 || k==79 || k==80 || k==81) && (j==61 || j==62 || j==63 || j==70 || j==71 || j==72 || j==79 || j==80 || j==81) && k~=j
            allconn(j,k)=1;
        end
    end
end
%print the connectivity matrix
allconn
% turn it into a graph so we can do math
sudokugraph = graph(allconn);
% make the x and y coordinates for each node so it can plot correctly
x = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9];
y = -1*[1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9];
%plot the graph
plot(sudokugraph,'XData',x,'YData',y)

%%
% assign each node to one of 9 colors
coloring = randi(9,[1,81])

%check if it works
%assume yes
works = true;
for k = 1:81
    for j = 1:81
        if allconn(j,k)==1 && coloring(k)==coloring(j)
            works = false;
        end
    end
end
works


% let's try putting it in a while loop
tries = 0;
works = false;
while works == false && tries < 5000
    % assign each node to one of 9 colors
    coloring = randi(9,[1,81]);

    %check if it works
    %assume yes
    works = true;
    for k = 1:81
        for j = 1:81
            if allconn(j,k)==1 && coloring(k)==coloring(j)
                works = false;
            end
        end
    end
    tries = tries+1;
end
works


%this doesn't work. What if we ensure that there's nine of each color?
duplicate=true;
tries = 0;
while duplicate==true && tries<1000
    duplicate=false;
    rand1s = randi(81,9);
    for k1=1:9
        for j1=1:9
            for k2=1:9
                for j2=1:9
                    if (k1==k2 && j1==j2)
                    elseif rand1s(k1,j1)==rand1s(k2,j2)
                        duplicate=true;
                    end
                end
            end
        end
    end
    tries = 1+ tries;
end
duplicate
% and it never finds one. great. Let's try a different method


% let's deal with each color separately
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
rand1s
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
rand2s
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
rand3s
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
rand4s
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
rand5s
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
rand6s
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
rand7s
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
rand8s
% do the coloring
for k = 1:9
    coloring(rand8s(k))=8;
end

for k=1:81
    if coloring(k)==0
        coloring(k)=9;
    end
end
coloring

% put this in a function so I can put it in a loop without it looking too
% bad

coloring = SudokuRandColoring()

%%
% This is a new section because the coloring section takes a while to run
% figure out how to plot the sudoku graph
ones = find(coloring==1)
twos = find(coloring==2)
threes = find(coloring==3)
fours = find(coloring==4)
fives = find(coloring==5)
sixes = find(coloring==6)
sevens = find(coloring==7)
eights = find(coloring==8)
nines = find(coloring==9)
plot(x(ones),y(ones),"Marker",".",LineStyle="none",MarkerSize=40)
hold on
plot(x(twos),y(twos),"Marker",".",LineStyle="none",MarkerSize=40)
plot(x(threes),y(threes),"Marker",".",LineStyle="none",MarkerSize=40)
plot(x(fours),y(fours),"Marker",".",LineStyle="none",MarkerSize=40)
plot(x(fives),y(fives),"Marker",".",LineStyle="none",MarkerSize=40)
plot(x(sixes),y(sixes),"Marker",".",LineStyle="none",MarkerSize=40)
plot(x(sevens),y(sevens),"Marker",".",LineStyle="none",MarkerSize=40)
plot(x(eights),y(eights),"Marker",".",LineStyle="none",MarkerSize=40)
plot(x(nines),y(nines),"Marker",".",LineStyle="none",MarkerSize=40)
plot([.5,9.5],[-3.5,-3.5],"k")
plot([.5,9.5],[-6.5,-6.5],"k")
plot([3.5,3.5],[-.5,-9.5],"k")
plot([6.5,6.5],[-.5,-9.5],"k")
plot([.5,9.5,9.5,.5,.5],[-.5,-.5,-9.5,-9.5,-.5],"k")
hold off
axis([0,10,-10,0])
title("Sudoku Coloring")

% yay it plots and it looks alright. Let's put it in a function so I can
% use it over and over again.
SudokuPlotColor(coloring,x,y)

% And now, we can put it all together in a giant for loop.

%%
% This is the giant for loop for putting it together. Basically, it's going
% to generate a coloring, plot it, check if it works, and then try again if
% it doesn't. That sounds like so much fun, right?
%debugging here
ones = find(coloring==1);

%define variables we need
x = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9];
y = -1*[1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9];

%start with defining works as false and our counter at 0
works = false;
counter = 0;
figure()
%then we do the while loop
while works==false && counter<1
    %we have to define works as true here
    works = true;
    coloring = SudokuRandColoring;
    for k = 1:81
        for j = 1:81
            if allconn(j,k)==1 && coloring(k)==coloring(j)
                works = false;
            end
        end
    end
    coloring;
    SudokuPlotColor(coloring,x,y)
    counter = counter +1;
end
works