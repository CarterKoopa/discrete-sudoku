function [] = SudokuPlotColor(coloring,x,y)
%SUDOKUPLOTCOLOR Plots the colored plot of a sudoku with the given
%colorings
%   Detailed explanation goes here
    ones = find(coloring==1);
    twos = find(coloring==2);
    threes = find(coloring==3);
    fours = find(coloring==4);
    fives = find(coloring==5);
    sixes = find(coloring==6);
    sevens = find(coloring==7);
    eights = find(coloring==8);
    nines = find(coloring==9);
    plot(x(ones),y(ones),"Marker",".",LineStyle="none",MarkerSize=40,Color="#005f73")
    hold on
    plot(x(twos),y(twos),"Marker",".",LineStyle="none",MarkerSize=40,color="#0a9396")
    plot(x(threes),y(threes),"Marker",".",LineStyle="none",MarkerSize=40,color="#94d2bd")
    plot(x(fours),y(fours),"Marker",".",LineStyle="none",MarkerSize=40,color="#e9d8a6")
    plot(x(fives),y(fives),"Marker",".",LineStyle="none",MarkerSize=40,color="#ee9b00")
    plot(x(sixes),y(sixes),"Marker",".",LineStyle="none",MarkerSize=40,color="#ca6702")
    plot(x(sevens),y(sevens),"Marker",".",LineStyle="none",MarkerSize=40,color="#bb3e03")
    plot(x(eights),y(eights),"Marker",".",LineStyle="none",MarkerSize=40,color="#ae2012")
    plot(x(nines),y(nines),"Marker",".",LineStyle="none",MarkerSize=40,color="#9b2226")
    plot([.5,9.5],[-3.5,-3.5],color="#001219")
    plot([.5,9.5],[-6.5,-6.5],color="#001219")
    plot([3.5,3.5],[-.5,-9.5],color="#001219")
    plot([6.5,6.5],[-.5,-9.5],color="#001219")
    plot([.5,9.5,9.5,.5,.5],[-.5,-.5,-9.5,-9.5,-.5],color="#001219")
    hold off
    axis([0,10,-10,0])
    title("Sudoku Coloring")
end