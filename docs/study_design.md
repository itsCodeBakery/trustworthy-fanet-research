# Research problem and scientific contract

**Status:** planned investigation, not a proven new method or an experimental result.  
**Source:** user-supplied 18 October 2026 *UAV_FANET_Research_Overleaf_Package.zip*; its Research Blueprint, Sections 1 and 4–9.

## Concrete problem

An honest upstream UAV hands packets to a next-hop relay. It can check some of the relay's transmissions using local packet headers and radio observations, but it cannot see the relay's internal queue or every over-the-air transmission. Wireless loss and monitor deafness may look like deliberate selective packet dropping. The goal is to identify *exposed* malicious packet discards promptly without falsely accusing honest relays when local evidence is weak.

## Proposed contributions (hypotheses, not achievements)

1. **Monitor-realistic benchmark:** generate independent FANET mission families that distinguish malicious network-layer drops, legitimate packet losses, missed forwarding witnesses, and unsuccessful handoffs, while keeping evaluator-only simulator truth isolated.
2. **Observation-aware decisions:** compare a causal benign predictor plus observation gate and sequential CUSUM against strong statistical and temporal baselines at **the same calibrated complete-mission false-accusation budget**.
3. **Measured network consequences:** quantify legitimate delivery and delay after temporary *local* avoidance of an accused next-hop relay in fresh closed-loop ns-3 runs, accounting for false isolation and route-repair cost.

These ingredients alone do not prove novelty; prior channel-aware selective-forwarding and early FANET classification methods must be audited before writing an exclusive contribution claim.

## Research questions

**RQ1:** At the same fixed-horizon all-benign false-accusation budget, does evidence-gated sequential detection identify exposed selective-forwarding attackers within 30 s better than channel-aware statistical detection and a temporal classifier?

**RQ2:** How do detection, alarm, delay, and deferral change under unseen missions, wireless-channel conditions, traffic loads, and attack schedules?

**RQ3:** Does a detection-triggered temporary local next-hop avoidance policy improve legitimate delivery and timely delivery after accounting for false accusations, outages, and route repair?

## Input and attacker boundary

Detector input is **locally available** successful MAC handoffs, observed forwarding witnesses (deduplicated by visible flow/sequence header), locally received beacons/RSSI and route/context measurements. Features must be causal and must not contain future packet observations, true simulator positions, malicious-drop reason logs, or attack identities.

The network-layer attacker can drop eligible forwarded data. It does not forge the trusted application packet identity, compromise the monitor, or control privileged simulation labels. Benign channel losses, congestion, monitoring gaps and route changes remain possible. A monitor that cannot associate forwarding under encryption needs an authorized receipt/visibility mechanism; that assumption must be disclosed.

## Proposed decision rule (development choices, not measured optima)

- Divide locally observed handoffs into 1 s windows. Use previous 16 windows for the benign predictor (no current outcome leakage).
- Let n be locally successful eligible handoffs whose observation deadline expired, and f be distinct packets whose matching forwarding was overheard by that deadline. The unmatched fraction is u=(n-f)/n for n>0; n=0 is *missing evidence*, never zero malicious dropping.
- A small causal TCN predicts benign unmatched probability q from past-only context. Compare with GLM and boosted benign predictors on the same information.
- Initially permit evidence accumulation only with at least 10 eligible handoffs, sufficiently recent beacon and own transmit-busy fraction <0.5; tune proxy thresholds on development data.
- Residual z=((n-f)-nq)/sqrt(nq(1-q)+1), clipped to [-10,10]; accumulator S=max(0,S_previous+z-kappa) while gate open, reset when gate closes. Development kappa candidates {0.25,0.5,1}.
- Output **no accusation**, **suspicious relay**, or **insufficient evidence**. No accusation does not prove a relay is innocent.
- Local response (if enabled): initial 10 s avoidance of one selected next-hop, with actual AODV reselection and outages recorded.

## Complete-mission alarm calibration

With model/gate/rule frozen, calculate one maximum score across pairs and times per **199 independent all-benign calibration missions**, each with H=600 s. For target alpha=0.05, use the ceil((B+1)(1-alpha))-th sorted maximum, or infinity if the index exceeds B. Accuse only on strictly greater score and an open gate. Also study alpha=0.01 and 0.10.

This fixed-horizon rank construction controls all-benign mission false accusations only under the necessary exchangeability/frozen-method assumptions; it is not a guarantee under arbitrary distribution shift, indefinite operation, or altered attack-time network traffic.

## Null and failure cases

If honest and malicious relays induce indistinguishable **local observation distributions**, a local classifier cannot reliably separate them. Report this uncertainty instead of leaking simulator-only truth. If a simpler statistical detector matches the proposed TCN, retain the simpler approach. If the gate suppresses most attack exposure or route avoidance harms delivery, report the limitation without claiming superiority.

**Next technical gate:** small ns-3 observability pilot confirming MAC handoffs and packet forwarding witnesses can actually be collected and matched.
