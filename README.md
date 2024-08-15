Design and Implementation of a Pipelined Reliable Transfer

Protocol
Introduction

In this project, we designed and implemented a transfer protocol using UDP sockets. The protocol incorporates mechanisms for flow control and congestion control to ensure reliable data transmission over an unreliable network. We also simulated packet loss and errors to test the robustness of our protocol.

Protocol Design
Our protocol is designed with the following key components:
1. Flow Control: Ensures that the sender does not overwhelm the receiver with too
many packets at once.
2. Congestion Control: Adjusts the sending rate based on network conditions to avoid
congestion.
3. Reliability: Implements acknowledgment and retransmission mechanisms to ensure
all packets are received correctly.
4. Connection Management: Establishes and closes connections to ensure reliable and
orderly data transfer.

Flow Control:
Flow control is managed using a sliding window mechanism. The sender maintains a window of packets that can be sent without waiting for an acknowledgment. The size of this window is dynamically adjusted based on acknowledgments received from the receiver.

Congestion Control:
Congestion control is implemented using a combination of Slow Start and Congestion
Avoidance algorithms. The sender starts with a small congestion window (cwnd) and
increases it exponentially during the slow start phase. Once the congestion window reaches a threshold (ssthresh), the window size is increased linearly to avoid congestion.
Packet Structure:
 Packet Type: Indicates whether the packet is a data packet, acknowledgment, or
control packet (e.g., SYN, ACK, FIN).
 Sequence Number: A unique identifier for each packet.
 Checksum: A 16-bit checksum for error detection.
 Payload: The actual data being transmitted.

Implementation
Sender (rdt_send):
The sender function, rdt_send, is responsible for sending packets to the receiver. It maintains the state of the sliding window and handles retransmissions in case of timeouts. The sender adjusts the congestion window size based on acknowledgments received. Additionally, the sender performs a three-way handshake to establish a connection before data transfer begins and a teardown procedure to close the connection after data transfer completes. 

Receiver (rdt_receive):
The receiver function, rdt_receive, receives packets, checks for errors using the checksum, and sends acknowledgments for correctly received packets. The receiver also handles out-oforder packets and ensures that duplicate packets are not processed. The receiver participates in the connection establishment and teardown processes by responding to SYN and FIN packets.

Connection Management:
The protocol includes mechanisms for establishing and closing connections:
 Three-Way Handshake: The connection is established using a SYN, SYN-ACK,
and ACK exchange.
 Teardown Procedure: The connection is closed using a FIN, FIN-ACK, and ACK
exchange.

Testing and Analysis
To test the protocol, we used Wireshark to capture and analyze the traffic. We verified that the protocol is connection-oriented and implements the designed flow and congestion control mechanisms effectively.

Connection oriented
The protocol initiates a connection with a three-way handshake, similar to TCP. The process involves:
 The sender sends an initial SYN packet to the receiver.
 The receiver responds with a SYN-ACK packet.
 The sender replies with an ACK packet, completing the handshake.
Wireshark Analysis:
- Packet 7: SYN packet from sender to receiver.
- Packet 8: SYN-ACK packet from receiver to sender.
- Packet 9: ACK packet from sender to receiver.

The protocol terminates the connection with a two-way handshake involving FIN packets.
The process ensures that both the sender and receiver agree to close the connection, thereby maintaining a reliable communication session.
 The sender initiates the termination by sending a FIN packet.
 The receiver acknowledges the FIN packet by sending a FIN packet in response.
 The sender completes the termination upon receiving the FIN packet from the
receiver.
Wireshark captures of the termination process:
- Packet 288: FIN packet from sender to receiver.
- Packet 289: FIN packet from receiver to sender.
The Wireshark capture shows the connection termination process
Acceptable performance
We can measure if the protocol has acceptable performance based on a lot of things. One of the ways is by analyzing the throughput.
Throughput
We can see that the protocol ranged 3-39 packets per second. In average that was around 9 packets per second. This indicates the efficiency of data transfer under varying network conditions.
Jitter
Jitter, which measures the variability in packet arrival times, is another crucial factor for assessing performance. In our analysis, the jitter was calculated to be 1.516912 seconds. This value reflects the variability in packet delays and can impact the overall performance and reliability of the protocol. Lower jitter values generally indicate a more stable and predictable network performance, which is essential for applications requiring consistent data transfer rates.
The protocol demonstrates acceptable performance by adjusting the sending rate based on network conditions.

Implements flow control
The protocol uses a sliding window mechanism to control the flow of data between the sender and receiver. The sender can transmit up to cwnd packets before needing an acknowledgment (ACK).

Implements congestion control
The sender’s congestion window (cwnd) starts with an initial value and adjusts according to the congestion control algorithm. In slow start, cwnd increases exponentially until it reaches a threshold (ssthresh). After that, it increases linearly to avoid congestion.

Packet Loss Simulation
1. Implementation: A probability-based approach was implemented where a certain
percentage of packets were randomly dropped during transmission. This was
achieved by generating a random number and comparing it to the loss probability
threshold.
2. Observation: The simulation demonstrated how well the protocol handles packet loss
by observing retransmissions and acknowledgments. We monitored whether the
sender retransmitted lost packets and how the receiver handled missing packets.

Packet Corruption Simulation
1. Implementation: Packet corruption was simulated by randomly altering the payload
of packets before sending them. A single bit of the payload was flipped to simulate
errors.
2. Observation: The protocol’s checksum mechanism was tested for its effectiveness in
detecting and handling corrupt packets. We observed how the receiver identified
corrupted packets and whether it requested retransmissions correctly.