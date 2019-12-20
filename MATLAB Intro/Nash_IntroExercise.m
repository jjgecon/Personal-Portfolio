%Code by Javier Gonzalez on October 2019
%For any questions please contact javierj.g18@gmail.com
%This code will calculate the Nash Equilibrium in a normal game 2x2 with
%only one equilibrium.

clear all
%insert the payout matrix
%let's do a 2x2 game, like a prisoners dilema
payoutmatrix = [-8 -8 0 -20 ; -20 0 -1 -1];
payoutmatrix = [1 1 0 0 ; -1 -1 2 2];
%each row its the action of player one
%each pair of colums 1-2 and 3-4 are players 2 actions
%each odd colums is the payout for player 1 due to action of the row 1
%while each even colum is the payout of 2 with the respective action of p2
%and p1

%Steps
%P1 best responses:
%for each row, fix a colum (1 or 3) and choose the maximun between rows
%then return the pair column and row.
%In this example the best response to action 1 of P2 is row1 should return 
%(1,1)
%For action 2 (columns 3-4) of player 2 the best response of P1 is 1, then
%it should return (1,2)

%P2 best responses:
%for each colum (2 or 4 cause we are on P2 side) fix a row and choose the
%maximun return.
%If P1 plays 1, P2 should play 1, then it returns (1,1)
%If P1 plays 2, P2 should play 1 to gain 0, there the algorithm should
%return the position (2,1)

%Then after all responses are recorded (should be 2x2), if two of them
%match then you found a Nash equilibrium. In this case the equilibrium
%should be (1,1), ergo we found a prisoners deilema.

% Functions needed:
% Matrix size, find, structure (positions)
% Simple for loops
% If statements
% Max function

%CODE ---------------------------------------------------------------------
%P1 best responses:
%P2 chosses Action 1
result = max(payoutmatrix(1,1),payoutmatrix(2,1));
findBR11 = find(payoutmatrix == result);
[r,c] = size(findBR11);
%lets make a matrix map
%payoutmatrix = [1 3 5 7; 
%                2 4 6 8]
%Im interested on the values of 1,2,5,6. Therefore, I should only record
%the 1 position. Because we fixes columns only 1 and 2 should be recorded

for i = 1:r
    if findBR11(i,1) == 1
        P1bestresponse1 = [1 1];
    elseif findBR11(i,1) == 2
        P1bestresponse1 = [2 1];
    end
end

%P2 chosses Action 2
result = max(payoutmatrix(1,3),payoutmatrix(2,3));
findBR12 = find(payoutmatrix == result);
[r,c] = size(findBR12);

for i = 1:r
    if findBR12(i,1) == 5
        P1bestresponse2 = [1 2];
    elseif findBR12(i,1) == 6
        P1bestresponse2 = [2 2];
    end
end

%P2 best responses:
%P1 chosses Action 1
result = max(payoutmatrix(1,2),payoutmatrix(1,4));
findBR21 = find(payoutmatrix == result);
[r,c] = size(findBR21);
%lets make a matrix map
%payoutmatrix = [1 3 5 7; 
%                2 4 6 8]
%Im interested on the values of 1,2,5,6. Therefore, I should only record
%the 1 position. Because we fixes columns only 1 and 2 should be recorded

for i = 1:r
    if findBR21(i,1) == 3
        P2bestresponse1 = [1 1];
    elseif findBR21(i,1) == 7
        P2bestresponse1 = [1 2];
    end
end

%P1 chosses Action 2
result = max(payoutmatrix(2,2),payoutmatrix(2,4));
findBR22 = find(payoutmatrix == result);
[r,c] = size(findBR22);

for i = 1:r
    if findBR22(i,1) == 4
        P2bestresponse2 = [2 1];
    elseif findBR22(i,1) == 8
        P2bestresponse2 = [2 2];
    end
end


%Finally we need to check if the bestresponces match
if P1bestresponse1 == P2bestresponse1 | P1bestresponse1 == P2bestresponse2
    z=['found a Nash Equilibrium at ', mat2str(P1bestresponse1)];
    disp(z)
end
if P1bestresponse2 == P2bestresponse1 | P1bestresponse2 == P2bestresponse2
    z=['found a Nash Equilibrium at ', mat2str(P1bestresponse2)];
    disp(z)
end
