function [Fit] = thermofit(T)
%{
Creates array based on NASA thermofit of H(T) and so(T) and Cp(T)
Array is in form [CO;CO2;O;O2] and [hf, H, So, Cp]
%}

%% Setup
R = 8.314; %KJ/kmolk-K
Fit = zeros(4,4);

%formation energy from Table A-26 Cengel % Boles
hf(1) = -110530; %kJ/kmol  CO
hf(2) = -393520; %kJ/kmol  CO2
hf(3) = 249175.003; %kJ/kmol  O
hf(4) = 0; %kJ/kmol  O2


% 1000 < T_expected < 6000 K (CO)

CO(1) = 4.619197250*10^5;
CO(2) = -1.944704863*10^3;
CO(3) = 5.916714180;
CO(4) = -5.664282830*10^-4;  
CO(5) = 1.398814540*10^-7;
CO(6) = -1.787680361*10^-11; 
CO(7) = 9.620935570*10^-16; 
CO(8) = -2.466261084*10^3;
CO(9) = -1.387413108*10^1;

% for 1000 < T_expected < 6000 K (CO2)

CO2(1) = 1.176962419*10^5;
CO2(2) = -1.788791477*10^3;
CO2(3) = 8.291523190;
CO2(4) = -9.223156780*10^-5;
CO2(5) = 4.863676880*10^-9;
CO2(6) = -1.891053312*10^-12;
CO2(7) = 6.330036590*10^-16;
CO2(8) = -3.908350590*10^4;
CO2(9) = -2.652669281*10^1;

% 1000 < T_expected < 6000 K (O)

O(1) = 2.619020262*10^5;
O(2) = -7.298722030*10^2;
O(3) = 3.317177270;
O(4) = -4.281334360*10^-4; 
O(5) = 1.036104594*10^-7;
O(6) = -9.438304330*10^-12;
O(7) = 2.725038297*10^-16;
O(8) = 3.392428060*10^4;
O(9) = -6.679585350*10^-1;
  
% 1000 < T_expected < 6000 K (O2)

O2(1) = -1.037939022*10^6;
O2(2) = 2.344830282*10^3;
O2(3) = 1.819732036;
O2(4) =  1.267847582*10^-3; 
O2(5) = -2.188067988*10^-7;
O2(6) = 2.053719572*10^-11;
O2(7) = -8.193467050*10^-16;
O2(8) = -1.689010929*10^4;
O2(9) = 1.738716506*10^1;

% Make full coefficient matrix for simple for loops
Coef = [CO;CO2;O;O2];

%% Find H and so
for j = 1:4
   
    Fit(j,1) = hf(j);
    
    %solve for H
    Fit(j,2) = R*T*(-Coef(j,1)*T^-2 + Coef(j,2)*log(T)*T^-1 + Coef(j,3) + ...
        ...
        Coef(j,4)*T/2 + Coef(j,5)*(T^2)/3 + Coef(j,6)*(T^3)/4 + ...
        ...
        Coef(j,7)*(T^4)/5 + Coef(j,8)/T);
    
    %solve for so
    Fit(j,3) = R*(-Coef(j,1)*(T^-2)/2 - Coef(j,2)*T^-1 + Coef(j,3)*log(T)+...
        ...
        Coef(j,4)*T + Coef(j,5)*(T^2)/2 + Coef(j,6)*(T^3)/3 + ...
        ...
        Coef(j,7)*(T^4)/4 + Coef(j,9));

    %solve for Cp
    Fit(j,4) = R*(Coef(j,1)*(T^-2) + Coef(j,2)*T^-1 + Coef(j,3)+...
        ...
        Coef(j,4)*T + Coef(j,5)*(T^2) + Coef(j,6)*(T^3) + ...
        ...
        Coef(j,7)*(T^4)); 
end

end

