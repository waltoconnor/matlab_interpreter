% SHAKESPEAREINSULT - returns a Shakespearian insult
% Downloaded from: https://www.mathworks.com/matlabcentral/fileexchange/68824-shakespeareinsult/
% Downloaded on: 2020-Dec-09
%	Removed function wrapper
%
%    Ever lost for words? ShakespeareInsult offers a random insult for every
%    occasion. S = ShakespeareInsult even returns the insult as a
%    character array S, thou, rank reeling-ripe nut-hook!
% 
%    Example:
%      ShakespeareInsult ; % could return ...
%      Thou, bawdy sheep-biting varlot!
%
%    See also WHY
% tested in Matlab R2018a
% version 1.1 (feb 2019)
% (c) Jos van der Geest
% email: samelinoa@gmail.com
% History
% Created (1.0) sep 2018
% 1.1 (sep 2018) - minor corrections in comments spelling
% 1.2 (feb 2019) - removed output when not asked for
% The insult is a random combination of three words, one from each column
% List copied from: 
% http://web.mit.edu/dryfoo/Funny-pages/shakespeare-insult-kit.html
% You can add your own adjectives and nouns, of course.
% ->  Thou, "adjective 1" "adjective 2" "noun"
 W = [ "artless", "base-court", "apple-john"; "bawdy", "bat-fowling", "baggage"; "beslubbering", "beef-witted", "barnacle"; "artless", "base-court", "apple-john"; "bawdy", "bat-fowling", "baggage"; "beslubbering", "beef-witted", "barnacle"; "bootless", "beetle-headed", "bladder"; "churlish", "boil-brained", "boar-pig"; "cockered", "clapper-clawed", "bugbear"; "clouted", "clay-brained", "bum-bailey"; "craven", "common-kissing", "canker-blossom"; "currish", "crook-pated", "clack-dish"; "dankish", "dismal-dreaming", "clotpole"; "dissembling", "dizzy-eyed", "coxcomb"; "droning", "doghearted", "codpiece"; "errant", "dread-bolted", "death-token"   ];

r1 = randi(0, size(W));
r2 = randi(0, size(W));
r3 = randi(0, size(W));

print(W(r1, 0) + W(r2, 1) + W(r3, 2));
 