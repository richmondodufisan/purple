
Order = 3;

% read the data of reference
name1 = ['Si_Ref_',num2str(Order),'.txt'];
[freq,t,c,cos,sin] = textread(name1,'%f %f %f %f %f');
freq = freq/10^6;
phase = atan2(sin,cos);
phase = phase./pi*180;
% phase = sin/10^6;
figure;plot(freq,phase);

% remove the discontinuity
phase = link(phase);
figure;
plot(freq,phase,'o','linewidth',1.5);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);
title('Reference Phase','fontsize',15);

% read the data of signal
name2 = ['Si_Signal_',num2str(Order),'.txt'];
[freq1,y,c,cos1,sin1] = textread(name2,'%f %f %f %f %f');
freq1 = freq1/10^6;
phase1 = atan2(sin1,cos1);
phase1 = phase1./pi*180;
% phase1 = sin1/10^6;
figure;plot(freq1,phase1);
% phase1(16) = phase1(16) + 360;
% % remove the discontinuity
% ind = find(freq1 == 70);
% phase1(1:ind(1)) = phase1(1:ind(1)) + phase1(ind(2)) - phase1(ind(1));
phase1 = link(phase1);
figure;
plot(freq1,phase1,'o','linewidth',1.5);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);
title('Measured Phase','fontsize',15);

figure;
plot(freq,phase,'o',freq1,phase1,'o','linewidth',1.5);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);
%legend({'reference phase','signal phase'},'fontsize',15);

difference = phase1 - phase ;
% hold on;plot(freq1,difference);
d = 28e-2;
c = 3e8;
phase_c = freq1*1e6*d/c*360;
difference_c = difference - phase_c;
figure;
% plot(freq,phase,freq,phase1,'--','linewidth',1.2);
% hold on;
plot(freq1,difference,'o','linewidth',1.5);
% hold on;
% plot(freq1,difference_c,'o','linewidth',1.5)
% legend({'Reference','Signal','Difference'},'fontsize',15);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);
%legend({'Phase difference','Phase difference after compensation'},'fontsize',15);

%P2 = detrend(phase1);

% figure;
% plot(freq1,a1,'o','linewidth',1.5)
% hold on
% plot(freq1,a2,'o','linewidth',1.5)
% figure;
% plot([10:4:150],P1,'o','linewidth',1.5);
% hold on
% plot([10:2:150],P1_2(1:71),'o','linewidth',1.5);
% legend({'Reference of this measurement','Data before'});
% xlabel('Frequency [MHZ]','fontsize',15);
% ylabel('Phase [deg]');