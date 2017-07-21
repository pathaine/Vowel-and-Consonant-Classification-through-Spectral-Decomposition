% CODE MODIFIED FROM: http://blogs.mathworks.com/cleve/2014/04/14/singular-value-analysis-of-cryptograms/

fid = fopen('english.txt');
k_letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'];
v = {'a','e','i','o','u'};
c = {'b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','x','z'};

%fid = fopen('french.txt');
%k_letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','à','â','æ','ç','é','è','ê','ë','î','ï','ô','œ','ù','û','ü'];
%v = {'a','e','i','o','u','à','â','æ','é','è','ê','ë','î','ï','ô','œ','ù','û','ü'};
%c = {'b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','x','z'};

%fid = fopen('greek.txt');
%k_letters = ['α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ','ν','ξ','ο','π','ρ','σ','ς','τ','υ','φ','χ','ψ','ω'];
%v = {'α','ε','η','ι','ο','υ','ω'};
%c = {'β','γ','δ','ζ','θ','κ','λ','μ','ν','ξ','π','ρ','σ','ς','τ','φ','χ','ψ'};

txt = fread(fid,'*char');
fclose(fid);
k = char(txt);
for i = 1:length(k_letters)
    k(k==k_letters(i)) = i;
end
k(k < 1 | k > length(k_letters)) = [];
j = k([2:length(k) 1]);
A = full(sparse(k,j,1,length(k_letters),length(k_letters)));
cnt = sum(A);
[U,S,V] = svd(A);
vowels = [];
consonants = [];
neuter = [];
for i = 1:length(k_letters)
   if cnt(i) > 0
      text(U(i,2),V(i,2),k_letters(i))
      if U(i,2) < 0 & V(i,2) > 0
          vowels{end + 1} = k_letters(i);
      elseif U(i,2) > 0 & V(i,2) < 0
          consonants{end + 1} = k_letters(i);
      else
          neuter{end + 1} = k_letters(i);
      end
   end
end
vowels
consonants
neuter
temp = consonants
consonants = vowels
vowels = temp
tp = intersect(vowels,v);            %true positive
tp = length(tp)
fp = intersect(consonants,v);		 %false positive
fp = length(fp)
fn = intersect(vowels,c);            %false negative
fn = length(fn)
tn = intersect(consonants,c);		 %true negative
tn = length(tn)

precision = tp/(tp+fp)
recall = tp/(tp+fn)
accuracy = (tp + tn)/(tp + tn + fp + fn)


fn = fn + length(neuter)            %false negative


precision = tp/(tp+fp)
recall = tp/(tp+fn)
accuracy = (tp + tn)/(tp + tn + fp + fn)

s = 4/3*max(max(abs(U(:,2))),max(abs(V(:,2))));
axis(s*[-1 1 -1 1])
axis square
line([0 0],[-s s],'color','b')
line([-s s],[0 0],'color','b')
box
title(sprintf('%d characters',length(k)))
