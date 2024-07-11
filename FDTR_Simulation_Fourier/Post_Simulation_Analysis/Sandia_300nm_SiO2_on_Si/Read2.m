clear
F = 1;
P =180*ones(1,65);
for Order =2:2
    
prefix = {'01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21'};   
name1 = ['Si_Ref00_',prefix{Order},'.txt'];
[freq,t,c,cos0,sin0] = textread(name1,'%f %f %f %f %f');
cos0 = 01*cos0;
sin0 = 01*sin0;
% read the data of reference
name1 = ['Si_Ref_',num2str(Order),'.txt'];
[freq,t,c,cos,sin] = textread(name1,'%f %f %f %f %f');
freq = freq/10^6;
phase = atan2(sin-sin0,cos-cos0);
phase = phase./pi*180;
% phase = sin/10^6;
figure;
subplot(2,3,1)
semilogx(freq,phase);

% remove the discontinuity
phase = link(phase);

subplot(2,3,2)
semilogx(freq,phase,'o','linewidth',1.5);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);
title('Reference Phase','fontsize',15);

% read the data of signal
name2 = ['Si_Signal_',num2str(Order),'.txt'];
[freq1,y,c,cos1,sin1] = textread(name2,'%f %f %f %f %f');
freq1 = freq1/10^6;
phase1 = atan2(sin1-sin0,cos1-cos0);
phase1 = phase1./pi*180;
% phase1 = sin1/10^6;

subplot(2,3,3)
semilogx(freq1,phase1);
% phase1(16) = phase1(16) + 360;
% % remove the discontinuity
% ind = find(freq1 == 70);
% phase1(1:ind(1)) = phase1(1:ind(1)) + phase1(ind(2)) - phase1(ind(1));
phase1 = link(phase1);

subplot(2,3,4)
plot(freq1,phase1,'o','linewidth',1.5);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);
title('Measured Phase','fontsize',15);

subplot(2,3,5)
plot(freq,phase,'o',freq1,phase1,'o','linewidth',1.5);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);
%legend({'reference phase','signal phase'},'fontsize',15);

difference = phase1 - phase - P(Order);
% hold on;plot(freq1,difference);
d = 28e-2;
c = 3e8;
phase_c = freq1*1e6*d/c*360;
difference_c = difference - phase_c;
subplot(2,3,6)
% plot(freq,phase,freq,phase1,'--','linewidth',1.2);
% hold on;
semilogx(freq1(1:end-1),link(difference(1:end-1)),'o','linewidth',1.5);
figure
semilogx(freq1(1:end-1),link(difference(1:end-1)),'o','linewidth',1.5);
% hold on;
% plot(freq1,difference_c,'o','linewidth',1.5)
% legend({'Reference','Signal','Difference'},'fontsize',15);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);
%legend({'Phase difference','Phase difference after compensation'},'fontsize',15);
set(gcf,'position',[200 200 1200 600]);
Phase_AuSiO2Si{Order} = link(difference);
Frequency_AuSiO2Si{Order} = freq1;
%P2 = detrend(phase1);
end
Tag = 'AuSiO2Si';
save(['Phase_',Tag],['Phase_',Tag]);
save(['Frequency_',Tag],['Frequency_',Tag]);

if F == 0
    figure
    hold on
    for i = 1:10
        plot(Frequency_AuSiO2Si{i},Phase_AuSiO2Si{i},'.','MarkerSize',12,'linewidth',1.5);
    end
    xlabel('Frequency [MHZ]');
    ylabel('Phase[Deg]');
    set(gca,'fontsize',15);
    box on
    set(gca,'fontweight','bold');
    legend({'1st','2nd','3rd'});
    title(Tag);
    saveas(gca,['FDTR_',Tag,'.png']);
    saveas(gca,['FDTR_',Tag,'.fig']);
end

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