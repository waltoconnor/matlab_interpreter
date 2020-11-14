function [Nj,Fit,N] = kramlich(P,T,phi)
% Kramlich N solver for CO + O2 combustion
%   Solves for N of elements for specified P and T

%% Setup and initial values
R = 8.314462618;
Po = 1;

%b is number of moles of element i in the system from input
b = [phi, phi+1]; % [C, O] from (phi*CO + 1/2 O2)

N = .1; %first iteration guess
NS = 4; %number of species (CO, CO2, O2, O)
Nj = ones(4,1)*N/NS; %first iteration guess for species

% Element to species relationship doesnt change
a = [1, 1, 0, 0; 1, 2, 1, 2];

% Setup inital error check
N_old = 0;
Nj_old = zeros(4,1);
g_old = zeros(4,1);


% Solve for hf,h-ho,so using NASA thermofit
Fit = thermofit(T);

% Initial g value
for j = 1:4
   g(j,1) = Fit(j,2) - T*Fit(j,3) + R*T*(log(Nj(j))-log(N) + log(P/Po));
end

%keeps track of total cycles
index = 0;

%% Iteration Loop STARTS HERE 
while index < 15
    % Find bo values

    for j = 1:2
        aN = 0;
        for k = 1:4
           aN = a(j,k)*Nj(k) + aN;
        end
        bo(j,1) = b(j) - aN;
    end

    %Find No value
    No = N - sum(Nj);

    % Setup matrix Ax = B
    a11 = eye(4);
    a12 = [-a(1,1), -a(2,1), -1; -a(1,2), -a(2,2), -1; -a(1,3), -a(2,3), -1; -a(1,4), -a(2,4), -1];
    a21 = [a(1,1)*Nj(1), a(1,2)*Nj(2), a(1,3)*Nj(3), a(1,4)*Nj(4); a(2,1)*Nj(1), a(2,2)*Nj(2), a(2,3)*Nj(3), a(2,4)*Nj(4); Nj(1), Nj(2), Nj(3), Nj(4)];
    a22 = [0, 0, 0; 0, 0, 0; 0, 0, -N];


    A = [a11, a12; a21, a22];
    B = [-g/(R*T); bo; No];

    X = A\B;

    %Adjusting parameter
    e1 = 2/max([5*abs(X(7)),abs(X(1:4)')]);

    e2 = ones(1,4);
    SIZE = -log(10^-8);
    for j = 1:4
        if log(Nj(j)/N)<-SIZE && X(j)>=0
            e2(j) = abs((-log(Nj(j)/N) - 9.2103404)/(X(j) - X(7)));
        end
    end

    %% Self-adjusting factor and iteration reset;
    e = min([1,e1,e2]);

    % Find new Values
    Nj_old = Nj;
    N_old = N;

    for j = 1:4
        Nj(j) = exp(log(Nj(j)) + e*X(j));
    end

    N = exp(log(N) + e*X(7));

    % Iteration test

    g_old = g;

    % Find new g values
    for j = 1:4
       g(j,1) =  Fit(j,2) - T*Fit(j,3) + R*T*(log(Nj(j))-log(N) + log(P/Po));
    end
    
    index = index + 1;
end

end



