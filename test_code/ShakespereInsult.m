function Sout = ShakespeareInsult
% SHAKESPEAREINSULT - returns a Shakespearian insult
% Downloaded from: https://www.mathworks.com/matlabcentral/fileexchange/68824-shakespeareinsult/
% Downloaded on: 2020-Dec-09
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
W = {
    'artless'     , 'base-court'     , 'apple-john'    ;
    'bawdy'       , 'bat-fowling'    , 'baggage'       ;
    'beslubbering', 'beef-witted'    , 'barnacle'      ;
    'bootless'    , 'beetle-headed'  , 'bladder'       ;
    'churlish'    , 'boil-brained'   , 'boar-pig'      ;
    'cockered'    , 'clapper-clawed' , 'bugbear'       ;
    'clouted'     , 'clay-brained'   , 'bum-bailey'    ;
    'craven'      , 'common-kissing' , 'canker-blossom';
    'currish'     , 'crook-pated'    , 'clack-dish'    ;
    'dankish'     , 'dismal-dreaming', 'clotpole'      ;
    'dissembling' , 'dizzy-eyed'     , 'coxcomb'       ;
    'droning'     , 'doghearted'     , 'codpiece'      ;
    'errant'      , 'dread-bolted'   , 'death-token'   ;
    'fawning'     , 'earth-vexing'   , 'dewberry'      ;
    'fobbing'     , 'elf-skinned'    , 'flap-dragon'   ;
    'froward'     , 'fat-kidneyed'   , 'flax-wench'    ;
    'frothy'      , 'fen-sucked'     , 'flirt-gill'    ;
    'gleeking'    , 'flap-mouthed'   , 'foot-licker'   ;
    'goatish'     , 'fly-bitten'     , 'fustilarian'   ;
    'gorbellied'  , 'folly-fallen'   , 'giglet'        ;
    'impertinent' , 'fool-born'      , 'gudgeon'       ;
    'infectious'  , 'full-gorged'    , 'haggard'       ;
    'jarring'     , 'guts-griping'   , 'harpy'         ;
    'loggerheaded', 'half-faced'     , 'hedge-pig'     ;
    'lumpish'     , 'hasty-witted'   , 'horn-beast'    ;
    'mammering'   , 'hedge-born'     , 'hugger-mugger' ;
    'mangled'     , 'hell-hated'     , 'joithead'      ;
    'mewling'     , 'idle-headed'    , 'lewdster'      ;
    'paunchy'     , 'ill-breeding'   , 'lout'          ;
    'pribbling'   , 'ill-nurtured'   , 'maggot-pie'    ;
    'puking'      , 'knotty-pated'   , 'malt-worm'     ;
    'puny'        , 'milk-livered'   , 'mammet'        ;
    'qualling'    , 'motley-minded'  , 'measle'        ;
    'rank'        , 'onion-eyed'     , 'minnow'        ;
    'reeky'       , 'plume-plucked'  , 'miscreant'     ;
    'roguish'     , 'pottle-deep'    , 'moldwarp'      ;
    'ruttish'     , 'pox-marked'     , 'mumble-news'   ;
    'saucy'       , 'reeling-ripe'   , 'nut-hook'      ;
    'spleeny'     , 'rough-hewn'     , 'pigeon-egg'    ;
    'spongy'      , 'rude-growing'   , 'pignut'        ;
    'surly'       , 'rump-fed'       , 'puttock'       ;
    'tottering'   , 'shard-borne'    , 'pumpion'       ;
    'unmuzzled'   , 'sheep-biting'   , 'ratsbane'      ;
    'vain'        , 'spur-galled'    , 'scut'          ;
    'venomed'     , 'swag-bellied'   , 'skainsmate'    ;
    'villainous'  , 'tardy-gaited'   , 'strumpet'      ;
    'warped'      , 'tickle-brained' , 'varlot'        ;
    'wayward'     , 'toad-spotted'   , 'vassal'        ;
    'weedy'       , 'unchin-snouted' , 'whey-face'     ;
    'yeasty'      , 'weather-bitten' , 'wagtail'       } ;
 r = randi(size(W,1),1,3) ;  % select three row indices
 % concatenate into a single string
 S = ['Thou, ' W{r(1),1} ' ' W{r(2),2} ' ' W{r(3),3} '!'] ;
 
 if ~nargout
     % no output argument, so just offer the insult
     disp(' ') ;
     disp(['  ' S]) ;
     disp(' ') ;
 else
     Sout = S ;
 end
 