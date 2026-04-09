# SDN-Flow-Timeout-Manager


# Problem Statement:
Explain:
-Implement flow rules with timeout in SDN and
Demonstrate idle and hard timeout behavior


# Objective:
--Understand SDN controller behavior
--Implement timeout-based flow rules
--Observe automatic flow deletion


# Tools Used:
--Mininet  
--POX Controller  
--OpenFlow  
--ovs-ofctl  


# Topology 
Single switch (s1) with 3 hosts (h1, h2, h3)


# How to Run:
#Run POX  
./pox.py misc.timeout_manager  
#Run Mininet  
sudo mn --topo single,3 --controller=remote  
(run on different terminals)


# Testing Scenarios:
-- Test 1: Normal Communication  
h1 ping h2 → flow installed  
-- Test 2: Idle Timeout  
Stop ping → wait 10 sec → flow removed  
-- Test 3: Hard Timeout  
Continuous ping → flow removed after 30 sec  


# Expected Output 
Flow rules appear and disappear based on timeout


# Conclusion
-SDN allows dynamic flow management  
-Timeout improves network efficiency  
