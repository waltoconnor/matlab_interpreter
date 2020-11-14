function [t, Comp] = ODEsolver(A,n,Ea,V,Bnry,init,tspan)
%ODESOLVER: Takes Reaction Coefficients and initial values as input 
%   Returns Composition matrix, total moles (M), Temperature, and
%   Pressure
%   Bnry input (1 or 0) enables/disables heat loss dq



%{
Setup ODE equations with Compositions in matrix y
This is in form: y = [n_CO, n_CO2, n_O, n_O2, M, T, P]'
%} 

R = 8.314;

[t,Comp] = ode15s(@(t,y) odefnct(t,y,A,n,Ea), tspan, init);

    function dydt = odefnct(t,y,A,n,Ea)
        [Fit] = thermofit(y(6));
        
        Kf = zeros(3,1);

        % Find K forward (Kf)
        for i = 1:3
            Kf(i) = A(i)*y(6)^n(i)*exp(-Ea(i)/(R*y(6)));
        end

        % Finding Kc


            % g_star = H - T*so
            g_star = zeros(4,1);

            for i = 1:length(g_star)
                g_star(i) = Fit(i,2) - y(6)*Fit(i,3);
            end

            % Gibbs of each reaction
            dG = zeros(3,1);

            dG(1) = g_star(2) - g_star(1) - g_star(3);
            dG(2) = g_star(2) + g_star(3) - g_star(1) - g_star(4);
            dG(3) = g_star(4) - 2*g_star(3);

            % Solve Kp
            for i = 1:length(dG)
               Kp(i) = exp(-dG(i)/(R*y(6)));
            end

        % Setup mole change for each reaction
        dn = [-1; 0; -1];

        % Kc = Kp / (RT/p_init)^dn
        Kc = zeros(3,1);

        for i = 1:length(Kp)
           Kc(i) = Kp(i) / ((R*y(6)/101325)^dn(i)); 
        end

        % Backwards reaction is Kf/Kc
        Kb = Kf./Kc;
        
        % U = H - RT
        for j = 1:length(Fit)
            U(j) = Fit(j,2) - R*y(6);
            Cv(j)= Fit(j,4) - R;
        end
        
        % Heat Loss from Bath
        T_oil = init(6);
        r = ((3*V)/(4*pi()))^(1/3); %V(m3)  r(m)
        k_oil = 0.100; % W/m-K
        dq = Bnry*4*pi()*r*k_oil*(y(6) - T_oil); %Binary for on or off
        
        % All functions are a combination of similar variables, simplify
        react_1 = Kf(1)*y(1)*y(3)*y(5);
        prod_1 = Kb(1)*y(2)*y(5);
        react_2 = Kf(2)*y(1)*y(4);
        prod_2 = Kb(2)*y(2)*y(3);
        react_3 = Kf(3)*y(3)*y(3)*y(5);
        prod_3 = Kb(3)*y(4)*y(5);
        
        % Setup actual ODE system with simplified code
        dydt = zeros(5,1);
        dydt(1) = -react_1 - react_2 + prod_1 + prod_2;
        dydt(2) = react_1 + react_2 - prod_1 - prod_2;
        dydt(3) = -react_1 + react_2 - 2*react_3 + prod_1 - prod_2 + 2*prod_3;
        dydt(4) = -react_2 + react_3 + prod_2 - prod_3;
        dydt(5) = dydt(1) + dydt(2) + dydt(3) + dydt(4);
        dydt(6) = -(dq/V + U(1)*dydt(1) + U(2)*dydt(2) + U(3)*dydt(3) + U(4)*dydt(4))/(Cv(1)*y(1)+ Cv(2)*y(2) + Cv(3)*y(3) + Cv(4)*y(4));
        dydt(7) = (dydt(5)*R*y(6) + y(5)*R*dydt(6));
    end
end

