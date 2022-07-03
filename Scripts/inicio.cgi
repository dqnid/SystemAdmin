#!/usr/bin/perl

use strict;
use warnings;

use CGI;
use CGI::Session;
use Linux::usermod;
use Authen::PAM;
use POSIX qw(ttyname);

my $q = CGI->new;
my $pamh;
my $session;

my $username = $q->param('usr');
my $password = $q->param('passw');

sub my_conv_func {
    my @res;
    while ( @_ ) {
        my $code = shift;
        my $msg = shift;
 	my $ans = '';

 		$ans = $username if ($code == PAM_PROMPT_ECHO_ON());
		if ($code == PAM_PROMPT_ECHO_OFF()){
 			$ans = $password 
		}
 
       push @res, (PAM_SUCCESS(),$ans);
    }
    push @res, PAM_SUCCESS();
    return @res;
}

if (!ref($pamh = new Authen::PAM("passwd", $username, \&my_conv_func))) {
    print "Authen::PAM error de inicio\n";
    print $q->redirect('/errorInicio.html');
    exit 1;
}

my $res = $pamh->pam_authenticate;

if($res == PAM_SUCCESS()){
    $session = CGI::Session->new();
    $session->save_param($q);
    $session->expires("+15m");
    $session->flush();
	system("/bin/bash /etc/Scripts/log.sh $username");
	print $q->redirect('/personal.html');
}else{
	print $q->redirect('/errorInicio.html');
}
