INtrution Detection Sytem 


Intrusion Detection System
Overview
With the rapid expansion of computer networks and the increase in the number of applications relying on them, ensuring network security has become critical. All computer systems have inherent security vulnerabilities, which are often complex and costly for manufacturers to address. This has amplified the importance of Intrusion Detection Systems (IDSs), which are specialized tools designed to identify anomalies and potential threats within a network.

Research in the field of intrusion detection has largely centered around two primary approaches: anomaly-based and misuse-based detection. Misuse-based detection is frequently favored in commercial products for its reliability and high accuracy, whereas anomaly detection is seen as a more advanced technique in academic circles due to its potential to identify previously unknown threats.

Despite numerous studies showing anomaly-based systems achieving high detection rates of up to 98% while maintaining a low false alarm rate of around 1%, practical implementations in commercial IDS solutions are rare. This disparity has prompted further investigations into the effectiveness of anomaly detection, analyzing aspects such as learning methods, training data, and evaluation techniques.

Business Problem
The goal of this project is to develop a network intrusion detection system capable of identifying anomalies and potential attacks. The project includes two main classification tasks:

Binary Classification: Determine if the network activity is normal or an attack.
Multiclass Classification: Categorize network activity as normal, or one of the following attack types: DOS, PROBE, R2L, or U2R.
Data Source
The data used for this project is sourced from the KDDCUP'99 dataset, a widely recognized dataset for network-based anomaly detection research. It includes a variety of features categorized as nominal, binary, or numeric.

Feature Types
Nominal: Protocol_type, Service, Flag
Binary: Land, logged_in, root_shell, su_attempted, is_host_login, is_guest_login
Numeric: Duration, src_bytes, dst_bytes, wrong_fragment, urgent, hot, num_failed_logins, num_compromised, num_root, num_file_creations, num_shells, num_access_files, num_outbound_cmds, count, srv_count, error_rate, srv_serror_rate, rerror_rate, srv_rerror_rate, same_srv_rate, diff_srv_rate, srv_diff_host_rate, dst_host_count, dst_host_srv_count, dst_host_same_srv_rate, dst_host_diff_srv_rate, dst_host_same_src_port_rate, dst_host_srv_diff_host_rate, dst_host_serror_rate, dst_host_srv_serror_rate, dst_host_rerror_rate, dst_host_srv_rerror_rate
Attack Types
The dataset is divided into several categories of attacks:

DoS (Denial of Service): Attacks that overwhelm resources to prevent legitimate access (e.g., SYN flooding). Key features include "source bytes" and "percentage of packets with errors".
Probe: Attacks aimed at gathering information about the network (e.g., port scanning). Key features include "connection duration" and "source bytes".
U2R (User to Root): Attacks involving the escalation of privileges on a local machine, starting from a standard user account to root/admin (e.g., buffer overflow). Key features include "number of file creations" and "number of shell prompts invoked".
R2L (Remote to Local): Attacks where an intruder gains access to a local machine from a remote location (e.g., password guessing). Key features involve network characteristics like "connection duration" and host-based details such as "number of failed login attempts".
Attack Classes & Subcategories
Below are the specific attack classes included in the dataset:

DoS (Denial of Service)
Examples: Back, Land, Neptune, Pod, Smurf, Teardrop, Apache2, Udpstorm, Processtable, Worm
Count: 10 types
Probe
Examples: Satan, Ipsweep, Nmap, Portsweep, Mscan, Saint
Count: 6 types
R2L (Remote to Local)
Examples: Guess_Password, Ftp_write, Imap, Phf, Multihop, Warezmaster, Warezclient, Spy, Xlock, Xsnoop, Snmpguess, Snmpgetattack, Httptunnel, Sendmail, Named
Count: 16 types
U2R (User to Root)
Examples: Buffer_overflow, Loadmodule, Rootkit, Perl, Sqlattack, Xterm, Ps
Count: 7 types
Conclusion
This project aims to leverage machine learning techniques to create a reliable and effective intrusion detection system capable of distinguishing between normal activity and various attack types. Through comprehensive analysis and model training, the objective is to improve the accuracy and applicability of IDSs, contributing to a safer network environment.

