%% Project1_2 
% By: Louis Bourque 260714602

% Setup values
phi = (.5:.1:2);
P = (0.25:0.25:10);
T_af = zeros(1,length(phi));
T_afP = zeros(1,length(P));
comp_phi = zeros(4,16);
comp_P = zeros(4,40);

% Call in values of NASA CEA solutions
NASA_CEA;


%% Solve for adiabatic temperatures through variation of phi
for i = 1:length(phi)

    % Initial Temperature guess
    T = 2750;
    
    % Find moles of each species along with thermofit H and S values
    [Nj,Fit,N] = kramlich(1,T,phi(i));
    
    % Combustion energy conservation
    LHS = phi(i)*Fit(1,1);
    RHS = Nj(1)*Fit(1,2) + Nj(2)*Fit(2,2) + Nj(3)*Fit(3,2) + Nj(4)*Fit(4,2);

    % Iterates through temperatures until conservation is met
    while abs(LHS - RHS) > 50
        T = T+.1;
        [Nj,Fit,N] = kramlich(1,T,phi(i));

        LHS = phi(i)*Fit(1,1);
        RHS = Nj(1)*Fit(1,2) + Nj(2)*Fit(2,2) + Nj(3)*Fit(3,2) + Nj(4)*Fit(4,2);
    end
    comp_phi(:,i) = [Nj(:)]/N;
    T_af(i) = T;
    i = i + 1;
end

% Displays found values in Table
Table1 = table(phi(:),T_af(:),comp_phi(1,:)',comp_phi(2,:)',comp_phi(3,:)',comp_phi(4,:)');
Table1.Properties.VariableNames = {'Phi' 'Adiabatic Temperature (K)' 'N_CO' 'N_CO2' 'N_O' 'N_O2'}


% Plots figures for program and CEA temperatures through varying phi
figure(1)
plot(phi,T_af,'--b')
grid on
hold on

plot(phi,NASA_phi,'m')
legend('Kramlich','NASA CEA T')
xlabel('Phi')
ylabel('Adiabatic Flame Temperature (K)')
title('Adiabatic Flame Temperature for Varying Phi CO Combustion')
hold off

figure(2)
grid on
hold on
plot(phi,comp_phi)
title('Mole Composition with Varying Phi')
xlabel('Phi')
ylabel('Molar mass percentage')
legend('CO','CO2','O','O2')

%% Solve for variations in P
for i = 1:length(P)

    % Initial Temperature guess
    T = 2750;
    
    % Find moles of each species along with thermofit H and S values
    [Nj,Fit,N] = kramlich(P(i),T,1);
    
    % Combustion energy conservation
    LHS = Fit(1,1);
    RHS = Nj(1)*Fit(1,2) + Nj(2)*Fit(2,2) + Nj(3)*Fit(3,2) + Nj(4)*Fit(4,2);

    % Iterates through temperatures until conservation is met
    while abs(LHS - RHS) > 50
        T = T+.1;
        [Nj,Fit,N] = kramlich(P(i),T,1);

        LHS = Fit(1,1);
        RHS = Nj(1)*Fit(1,2) + Nj(2)*Fit(2,2) + Nj(3)*Fit(3,2) + Nj(4)*Fit(4,2);
    end
    T_afP(i) = T;
    comp_P(:,i) = [Nj(:)]/N;
    i = i + 1;
end

% Displays found values in Table
Table2 = table(P(:),T_afP(:), comp_P(1,:)',comp_P(2,:)',comp_P(3,:)',comp_P(4,:)');
Table2.Properties.VariableNames = {'Pressure (atm)' 'Adiabatic Temperature (K)' 'N_CO' 'N_CO2' 'N_O' 'N_O2'}

figure(3)
plot(P,T_afP,'--b')
grid on
hold on

plot(P,NASA_P,'m')
legend('Kramlich','NASA CEA T')
xlabel('Pressure (atm)')
ylabel('Adiabatic Flame Temperature (K)')
title('Adiabatic Flame Temperature for Carying Pressure CO Combustion')

figure(4)
grid on
hold on
plot(P,comp_P)
title('Mole Composition with Varying Pressure')
xlabel('Pressure (atm)')
ylabel('Molar mass percentage')
legend('CO','CO2','O','O2')


%% Varying Pressure and phi

P_phi = [.5,1,5,10];
T_combined = zeros(4,16);

for j = 1:length(P_phi)
    
    for i = 1:length(phi)

        % Initial Temperature guess
        T = 2750;

        % Find moles of each species along with thermofit H and S values
        [Nj,Fit,N] = kramlich(P_phi(j),T,phi(i));

        % Combustion energy conservation
        LHS = phi(i)*Fit(1,1);
        RHS = Nj(1)*Fit(1,2) + Nj(2)*Fit(2,2) + Nj(3)*Fit(3,2) + Nj(4)*Fit(4,2);

        % Iterates through temperatures until conservation is met
        while abs(LHS - RHS) > 50
            T = T+.1;
            [Nj,Fit,N] = kramlich(P_phi(j),T,phi(i));

            LHS = phi(i)*Fit(1,1);
            RHS = Nj(1)*Fit(1,2) + Nj(2)*Fit(2,2) + Nj(3)*Fit(3,2) + Nj(4)*Fit(4,2);
        end
        
        T_combined(j,i) = T;
        i = i + 1;
    end
    j = j+1;
end

figure (5)
grid on
hold on
plot(phi, T_combined);
title('Affect of Varying Pressures on CO Combustion')
xlabel('Phi')
ylabel('Adiabatic Temperature (K)')
legend('.5 atm','1 atm', '5 atm', '10 atm')


%% Varying phi and Pressure

phi_P = [.5,1,2];
T_combined2 = zeros(1,40);

for j = 1:length(phi_P)
    
    for i = 1:length(P)

        % Initial Temperature guess
        % Due to lowered phi, initial guess is also lower
        T = 2300;

        % Find moles of each species along with thermofit H and S values
        [Nj,Fit,N] = kramlich(P(i),T,phi_P(j));

        % Combustion energy conservation
        LHS = phi_P(j)*Fit(1,1);
        RHS = Nj(1)*Fit(1,2) + Nj(2)*Fit(2,2) + Nj(3)*Fit(3,2) + Nj(4)*Fit(4,2);

        % Iterates through temperatures until conservation is met
        while abs(LHS - RHS) > 50
            T = T+.1;
            [Nj,Fit,N] = kramlich(P(i),T,phi_P(j));

            LHS = phi_P(j)*Fit(1,1);
            RHS = Nj(1)*Fit(1,2) + Nj(2)*Fit(2,2) + Nj(3)*Fit(3,2) + Nj(4)*Fit(4,2);
        end
        
        T_combined2(j,i) = T;
        i = i + 1;
    end
    j = j+1;
end

figure (6)
grid on
hold on
plot(P, T_combined2);
title('Affect of Varying Phi on CO Combustion')
xlabel('Pressure (atm)')
ylabel('Adiabatic Temperature (K)')
legend('.5','1', '2')

