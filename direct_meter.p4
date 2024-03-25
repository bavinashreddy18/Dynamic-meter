/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;
const bit<4> MAX_PORT = 15;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    tos;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}


struct metadata {
    bit<32> meter_tag;

 }



struct headers {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,

                out headers hdr,

                inout metadata meta,

                inout standard_metadata_t standard_metadata) {

 

    state start {

        transition parse_ethernet;

    }

 

    state parse_ethernet {

        packet.extract(hdr.ethernet);

        transition select(hdr.ethernet.etherType) {

            TYPE_IPV4: parse_ipv4;

            default: accept;

        }

    }

 

    state parse_ipv4 {

        packet.extract(hdr.ipv4);

        transition accept;

    }

 

}

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata){

    direct_meter<bit<32>>(MeterType.packets) my_meter;

    action drop() {
        mark_to_drop(standard_metadata);
    }  

    action m_action() {
        my_meter.read(meta.meter_tag);
    }

    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {

        // Set the src mac address as the previous dst, this is not correct right?
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;

        // Set the destination mac address that we got from the match in the table
        hdr.ethernet.dstAddr = dstAddr;

        // Set the output port that we also get from the table
        standard_metadata.egress_spec = port;

        // Decrease ttl by 1
        hdr.ipv4.ttl = hdr.ipv4.ttl -1;
    }

    table ipv4_lpm {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = NoAction();
    }

    table m_read {
        key = {
            hdr.ethernet.srcAddr: exact;
        }
        actions = {
            m_action;
            NoAction;
        }
        default_action = NoAction;
        meters = my_meter;
        size = 16384;
    }

    table m_filter {
        key = {
            meta.meter_tag: exact;
        }
        actions = {
            drop;
            NoAction;
        }
        default_action = drop;
        size = 16;
    }

    apply {
        // Only if IPV4 the rule is applied. Therefore other packets will not be forwarded.
                // Same egress port for all packets in this example
        standard_metadata.egress_spec = 2;

        // Check meter
        m_read.apply();

        // Filter based on meter status
        m_filter.apply();




        if (hdr.ipv4.isValid()){
            ipv4_lpm.apply();
            if (hdr.ipv4.tos == 0 || hdr.ipv4.tos == 1 || hdr.ipv4.tos == 2){
                standard_metadata.priority = (bit<3>)0;}
            // Packets from 10.0.1.2 get highest priority (7)
            else if (hdr.ipv4.tos == 5){
                standard_metadata.priority = (bit<3>)1;}
            else if (hdr.ipv4.tos == 3){
                standard_metadata.priority = (bit<3>)2;}
            else if (hdr.ipv4.tos == 4){
                standard_metadata.priority = (bit<3>)3;}
            else if (hdr.ipv4.tos == 6 ){
                standard_metadata.priority = (bit<3>)4;}
            else if (hdr.ipv4.tos == 7){
                standard_metadata.priority = (bit<3>)5;
            }
        }
    }
}

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {

	 counter((bit<32>)MAX_PORT, CounterType.bytes) egressPortCounter;


   apply {
        
        egressPortCounter.count((bit<32>)standard_metadata.egress_port);
        hdr.ipv4.tos = (bit<8>)standard_metadata.qid;

        }
    }
    

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
     apply {
	update_checksum(
	    hdr.ipv4.isValid(),
            { hdr.ipv4.version,
	      hdr.ipv4.ihl,
              hdr.ipv4.tos,
              hdr.ipv4.totalLen,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.srcAddr,
              hdr.ipv4.dstAddr },
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16);
    }
}


/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {

        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);

    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

//switch architecture
V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
