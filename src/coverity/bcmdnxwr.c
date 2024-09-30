INT4
NpWrFsMplsHwVpwsCreatePwVc (UINT4 u4VpnHwId, tMplsHwVcTnlInfo * pMplsHwVcInfo)
{
#ifdef Q2C_WANTED
    UINT4 u4VlanTranslationMode = 0;
    UINT4 u4Flag = 0;
    bcm_port_tpid_class_t portTpidClass;
#endif

    bcm_mpls_port_t     pwInfo;
    bcm_port_t          i4PortNum = 0;
    bcm_gport_t         pwOutGPort = 0;
    bcm_mac_t           BcmMacAddr;
    bcm_l2_addr_t       sBcmL2Addr;
    tMplsPwVpMapInfo    MplsPwVpMapInfo;
    tMplsPwVpMapInfo    *pMplsPwVpMapInfo = NULL;
    tQoSHwVpnProfileMap *pQoSHwVpnProfileMapNode = NULL;
    INT4                i4RetVal = BCM_E_NONE;
    INT4                i4UnitId = 0;
    INT4                i4IngExpMapId = 0;
    INT4                i4EgrExpMapId = 0;
    UINT4               u4AcPort = 0;
    UINT4               u4PwVpId = 0;
    UINT4               u4PwIfIndex = 0;
    UINT4               u4AcGport = 0;
    UINT4               u4PwVcIndex = 0;
    UINT4               u4VpnId = 0;
    DBG_MSG_ENTRY (NPAPI_MPLS, CLI_ISS_NP_LOG_DEBUG_LEVEL,
                   ("NpWrFsMplsHwVpwsCreatePwVc Called \n"));
    UNUSED_PARAM (u4PwVpId);

    bcm_mpls_port_t_init (&pwInfo);
    MEMSET (&MplsPwVpMapInfo, 0, sizeof (tMplsPwVpMapInfo));

    u4VpnId = u4VpnHwId;
    ISS_BCM_GET_VPN_ID_FROM_HW_VPN_ID (u4VpnId);
    if (pMplsHwVcInfo->u4PwOutPort != 0)
    {
        i4UnitId = CFA_NP_UNIT_ID (pMplsHwVcInfo->u4PwOutPort);
        i4PortNum = CFA_NP_PORT_NUM (pMplsHwVcInfo->u4PwOutPort);
    }
    else
    {
        /* Since the port on which the MAC address is learnt is not
         * available in control plane, the port is retrived from hardware.*/
        NP_FOR_ALL_UNITS (MBSM_SLOT_ALL, i4UnitId)
        {
            MEMSET (BcmMacAddr, 0, sizeof (bcm_mac_t));
            bcm_l2_addr_t_init (&sBcmL2Addr, BcmMacAddr, 0);
            i4RetVal = bcm_l2_addr_get (i4UnitId, pMplsHwVcInfo->au1PwDstMac,
                                        pMplsHwVcInfo->u2OutVlanId,
                                        &sBcmL2Addr);
            if (i4RetVal != BCM_E_NONE)
            {
                continue;
            }

            if ((sBcmL2Addr.flags & BCM_L2_TRUNK_MEMBER) != BCM_L2_TRUNK_MEMBER)
            {
                i4PortNum = sBcmL2Addr.port;
            }
            else
            {
                /* LAG support need to be provided. */
            }
            break;
        }

        if (i4RetVal != BCM_E_NONE)
        {
            NP_DEBUG_TRC1 (CLI_ISS_NP_LOG_ERROR_LEVEL, NPAPI_MPLS,
                           "\r\n NpWrFsMplsHwVpwsCreatePwVc : bcm_l2_address get "
                           "failed : %s\r\n", bcm_errmsg (i4RetVal));
            DBG_MSG_EXIT (NPAPI_MPLS, CLI_ISS_NP_LOG_DEBUG_LEVEL);
            return FNP_FAILURE;
        }
    }

    /* Get the the Global port for the Pseudowire underlying 
     * outbound tunnel outgoing port. */
    i4RetVal = bcm_port_gport_get (i4UnitId, i4PortNum, &pwOutGPort);
    if (i4RetVal != BCM_E_NONE)
    {
        NP_DEBUG_TRC3 (CLI_ISS_NP_LOG_ERROR_LEVEL, NPAPI_MPLS,
                       "\rFsMplsHwVpwsCreatePwVc: bcm_port_gport_get failed for PW out"
                       "port %d in unit %d with error %s", i4PortNum, i4UnitId,
                       bcm_errmsg (i4RetVal));
        DBG_MSG_EXIT (NPAPI_MPLS, CLI_ISS_NP_LOG_DEBUG_LEVEL);
        return FNP_FAILURE;
    }

    u4PwIfIndex = pMplsHwVcInfo->u4PwIfIndex;
    u4PwVcIndex = pMplsHwVcInfo->u4PwIndex;
   
    /* Get the PW Hw Id  for VPLS */
    ISS_BCM_GET_VP_FROM_INDEX (u4PwIfIndex, u4PwVcIndex, u4AcPort, 0);
    if (u4PwIfIndex != 0)
    {
        u4PwVpId = u4PwIfIndex;
    }
    else if (u4PwVcIndex != 0)
    {
        u4PwVpId = u4PwVcIndex;
    }
    else
    {
        NP_DEBUG_TRC2 (CLI_ISS_NP_LOG_ERROR_LEVEL, NPAPI_MPLS,
                       "NpWrFsMplsHwVpwsCreatePwVc: No Valid Virtual Port for the given"
                       "PW ifIndex : %d and PW Index : %d \r\n",
                       pMplsHwVcInfo->u4PwIfIndex, pMplsHwVcInfo->u4PwIndex);
        DBG_MSG_EXIT (NPAPI_MPLS, CLI_ISS_NP_LOG_DEBUG_LEVEL);
        return FNP_FAILURE;
    }

    pMplsPwVpMapInfo = NpUtilMplsGetPwInfoFromVp (u4PwVpId);
    if(pMplsPwVpMapInfo != NULL)
    {
        pMplsHwVcInfo->u4VcGport = pMplsPwVpMapInfo->u4VirtualPort;
        pMplsHwVcInfo->u4PwFecGport = pMplsPwVpMapInfo->u4FecGport;

        FsMplsHwVpwsDeletePwVc(u4VpnHwId,pMplsHwVcInfo);
    }
    /* Update the PW Info with PW VP Id, Physical Port of the 
     * underlying tunnel, egress object of the tunnel and the 
     * outgoing label information to create the VP for PW. */

    pwInfo.flags = (BCM_MPLS_PORT_EGRESS_TUNNEL | BCM_MPLS_PORT_INT_PRI_MAP);

    /* BCM_MPLS_PORT_WITH_ID is not supported in DNX*/
    /* Generated mpls_port_id will be used as key to database */
    pwInfo.mpls_port_id = (bcm_port_t)u4PwVpId;
    NP_DEBUG_TRC1 (CLI_ISS_NP_LOG_DEBUG_LEVEL, NPAPI_MPLS,
                   "\rFsMplsHwCreatePwVc: Key to DB:%d\r\n",
                   pwInfo.mpls_port_id);

    /* Update the PW Info with PW control word and sequence number
     * flags for underlying PW tunnel before programming the target.
     * This is for RFC4385 VPWS control word porting. */

    if(pMplsHwVcInfo->i1CwStatus == L2VPN_PWVC_CWPRESENT)
    {
       pwInfo.flags |= BCM_MPLS_PORT_CONTROL_WORD;
       pwInfo.flags |= BCM_MPLS_PORT_SEQUENCED;
    pwInfo.flags |=BCM_MPLS_PORT_NETWORK;
    pwInfo.flags |= BCM_MPLS_PORT_CONTROL_WORD;
    pwInfo.network_group_id =  1;
	}
    pwInfo.port = pwOutGPort;
    pwInfo.qos_map_id = i4IngExpMapId;

    /* Egress object ENCPAP ID */
    /* This code is added for MPLS LSP Proection switching with ELPS
       ELPS protection is done using Egress object.
       Hence only this method should be followed so that the pseudowire automatically 
       switches from working LSP to  protection LSP
     */
    if (NP_CFA_GET_HW_EGR_OBJ_INTF_FOR_VLAN_ID (pMplsHwVcInfo->u4PwL3Intf) !=
        FNP_ZERO)
    {
        pwInfo.egress_tunnel_if =
            NP_CFA_GET_HW_EGR_OBJ_INTF_FOR_VLAN_ID (pMplsHwVcInfo->u4PwL3Intf);
    }
    else
    {
        pwInfo.egress_tunnel_if =
            NP_CFA_GET_HW_EGR_OBJ_ID_FOR_VLAN_ID (pMplsHwVcInfo->u4PwL3Intf);
    }
    pwInfo.tunnel_id = NP_CFA_GET_HW_EGR_OBJ_ID (pMplsHwVcInfo->u4PwL3Intf);

    pwInfo.egress_label.flags = (BCM_MPLS_EGRESS_LABEL_TTL_SET |
                                 BCM_MPLS_EGRESS_LABEL_EXP_REMARK);
    pwInfo.egress_label.label = pMplsHwVcInfo->PwOutVcLabel.u.MplsShimLabel;
    /* TTL is updated to a default value. */
    pwInfo.egress_label.ttl = 255;
    pwInfo.egress_label.pkt_pri = 0;
    pwInfo.egress_label.pkt_cfi = 0;

    pwInfo.egress_label.qos_map_id = i4EgrExpMapId;

    /* Incoming Label Information for the PW. */
    pwInfo.criteria = BCM_MPLS_PORT_MATCH_LABEL;
    pwInfo.match_label = pMplsHwVcInfo->PwInVcLabel.u.MplsShimLabel;
    /* PW Support done over Router port */
    if (pMplsHwVcInfo->u2OutVlanId == FNP_ZERO)
    {
        pMplsHwVcInfo->u2OutVlanId =
            FsNpGetDummyVlanId (pMplsHwVcInfo->u4PwOutPort);
    }

    if (NpWrBcmMplsTnlEnable ((UINT4) pMplsHwVcInfo->u2OutVlanId) !=
        FNP_SUCCESS)
    {
        NP_DEBUG_TRC (CLI_ISS_NP_LOG_ERROR_LEVEL, NPAPI_MPLS,
                      "\r\n NpWrBcmMplsTnlEnable " "failed \r\n");
        DBG_MSG_EXIT (NPAPI_MPLS, CLI_ISS_NP_LOG_DEBUG_LEVEL);
        return FNP_FAILURE;
    }
    NP_FOR_ALL_UNITS (MBSM_SLOT_ALL, i4UnitId)
    {
        /* for VPWS VPN-ID will be zero*/
        i4RetVal = bcm_mpls_port_add (i4UnitId, FNP_ZERO, &pwInfo);
        if (i4RetVal != BCM_E_NONE)
        {
            NP_DEBUG_TRC3 (CLI_ISS_NP_LOG_ERROR_LEVEL, NPAPI_MPLS,
                           "\r FsMplsHwCreatePwVc : Adding PW %u to VPN %u failed"
                           " with error %s\r\n", pMplsHwVcInfo->u4PwIndex,
                           u4VpnHwId, bcm_errmsg (i4RetVal));
            DBG_MSG_EXIT (NPAPI_MPLS, CLI_ISS_NP_LOG_DEBUG_LEVEL);
            return FNP_FAILURE;
        }
        pwInfo.flags = BCM_MPLS_PORT_WITH_ID;
#ifdef Q2C_WANTED

        /* Use following API when bcm886xx_vlan_translate_mode is set */
        u4VlanTranslationMode =
            soc_property_get(i4UnitId , "bcm886xx_vlan_translate_mode",
                    FNP_ZERO);
        if( u4VlanTranslationMode )
        {
            bcm_port_tpid_class_t_init(&portTpidClass);
            portTpidClass.port = i4PortNum;
            /* u4Flag is set to 0 for DISCARD NONE scenario to accept all
               packets.*/
            if(u4Flag == FNP_ZERO)
            {
                portTpidClass.flags = BCM_PORT_DISCARD_NONE;
                portTpidClass.tpid1 = BCM_PORT_TPID_CLASS_TPID_ANY;
                portTpidClass.tpid2 = BCM_PORT_TPID_CLASS_TPID_ANY;
            }
            else
            {
                portTpidClass.flags = BCM_PORT_TPID_CLASS_DISCARD;
                portTpidClass.tpid1 = BCM_PORT_TPID_CLASS_TPID_INVALID;
                portTpidClass.tpid2 = BCM_PORT_TPID_CLASS_TPID_INVALID;
            }
            portTpidClass.vlan_translation_action_id = 0;
            portTpidClass.tag_format_class_id = 0;
            i4RetVal = bcm_port_tpid_class_set(i4UnitId, &portTpidClass);
        }
#else
        bcm_port_discard_set (i4UnitId, pwInfo.mpls_port_id,
                              BCM_PORT_DISCARD_NONE);
#endif
		/* Store PW LIF ID against the VPN ID */
    }
 if(pMplsHwVcInfo->u1PwRedflag == FNP_ZERO)
 {
    /* This Wrapper function in called for only DNX and not for XGS */
        i4RetVal =
            NpWrBcmMplsCreateFecPwVc (&pwInfo, pMplsHwVcInfo, pwOutGPort);
    if (i4RetVal != FNP_SUCCESS)
    {
	    NP_DEBUG_TRC (CLI_ISS_NP_LOG_ERROR_LEVEL, NPAPI_MPLS,
			    "\rFsMplsHwCreatePwVc: Adding PW info in RBTree failed\r\n ");
	    DBG_MSG_EXIT (NPAPI_MPLS, CLI_ISS_NP_LOG_DEBUG_LEVEL);
	    return FNP_FAILURE;
    }

    NP_DEBUG_TRC1 (CLI_ISS_NP_LOG_DEBUG_LEVEL, NPAPI_MPLS,
                       "\rFsMplsHwCreatePwVc: Pw VP:%d\r\n",
                       pwInfo.mpls_port_id);
    u4VpnId = u4VpnHwId;
    ISS_BCM_GET_VPN_ID_FROM_HW_VPN_ID (u4VpnId);
 }
    if (CFA_NP_IS_VEP_PORT (pMplsHwVcInfo->FecInfo.u4VpnSrcPhyPort) == FNP_TRUE)
    {
        NpUtilGetLifIndexFromVepIndex (pMplsHwVcInfo->FecInfo.u4VpnSrcPhyPort,
                                       &u4AcGport);
    }
    /*ISS generated LIF ID will be used as key to RB Tree*/
    MplsPwVpMapInfo.u4VirtualPort = (bcm_port_t)u4PwVpId;
    /* AC port is also stored here. This will be used when cross connect is deleted and recreated 
       when ELPS LSP protection is enabled
     */
    MplsPwVpMapInfo.u4VpwsCCAcGport = (bcm_port_t) u4AcGport;
    MplsPwVpMapInfo.u4VpnId = u4VpnId;
    MplsPwVpMapInfo.u4EgrObj = pwInfo.egress_tunnel_if;
    MplsPwVpMapInfo.u4EgrOutGPort = pwInfo.port;
    MplsPwVpMapInfo.u4FecGport = pMplsHwVcInfo->u4PwFecGport;
    MplsPwVpMapInfo.u4PwL3Intf = pMplsHwVcInfo->u4PwL3Intf;
    MplsPwVpMapInfo.u4TnlInLabel =
        pMplsHwVcInfo->MplsLabelList[0].u.MplsShimLabel;

    /*Save the hardware created LIF ID*/
    MplsPwVpMapInfo.u4PwVcGport = pwInfo.mpls_port_id;
    pMplsHwVcInfo->u4VcGport = pwInfo.mpls_port_id;

    /* Store Pseudowire information required for other modules. */
    pMplsPwVpMapInfo =
        NpUtilMplsGetPwInfoFromVp (MplsPwVpMapInfo.u4VirtualPort);
    if(pMplsPwVpMapInfo != NULL)
    {
      NpUtilMplsPwInfoDelete (pMplsPwVpMapInfo, TRUE);
    }

    i4RetVal = NpUtilMplsPwInfoAdd (&MplsPwVpMapInfo, TRUE);
    if (i4RetVal != FNP_SUCCESS)
    {
        NP_DEBUG_TRC (CLI_ISS_NP_LOG_ERROR_LEVEL, NPAPI_MPLS,
                      "\rFsMplsHwCreatePwVc: Adding PW info in RBTrees failed\r\n ");
        DBG_MSG_EXIT (NPAPI_MPLS, CLI_ISS_NP_LOG_DEBUG_LEVEL);
        return FNP_FAILURE;
    }

    pQoSHwVpnProfileMapNode = NpUtilQoSGetVpnProfileMap (u4VpnId, QOS_L2VPN);
    if (pQoSHwVpnProfileMapNode != NULL)
    {
        i4IngExpMapId = pQoSHwVpnProfileMapNode->u4HwIngProfileId;
        i4EgrExpMapId = pQoSHwVpnProfileMapNode->u4HwEgrProfileId;
        if (i4IngExpMapId != 0)
		{
			if (NpWrBcmMplsUpdtTnlSwitch 
                (0, pMplsHwVcInfo->MplsLabelList[0].u.MplsShimLabel,
                 i4IngExpMapId) == FNP_FAILURE)
			{
				NP_DEBUG_TRC1 (CLI_ISS_NP_LOG_ERROR_LEVEL, NPAPI_MPLS,
						"\r NpWrFsMplsHwVpwsCreatePwVc : Updating tunnel switch"
                               " with ingress profile id failed L3Intf=%d\r\n",
                               pMplsHwVcInfo->u4PwL3Intf);
				DBG_MSG_EXIT (NPAPI_MPLS, CLI_ISS_NP_LOG_DEBUG_LEVEL);
			}
		}
        if (i4EgrExpMapId != 0)
		{
			NP_FOR_ALL_UNITS (MBSM_SLOT_ALL, i4UnitId)
			{
				if (NpWrQosIvrProfileSet (i4UnitId, pMplsHwVcInfo->u4PwL3Intf,
                                          i4EgrExpMapId,
                                          QOS_EGRESS_EXP_SET_INTERFACE) ==
                    FNP_FAILURE)
				{
					NP_DEBUG_TRC1 (CLI_ISS_NP_LOG_ERROR_LEVEL, NPAPI_MPLS,
							"\r NpWrFsMplsHwVpwsCreatePwVc : Updating tunnel initiator"
                                   " with egress profile id failed L3Intf=%d\r\n",
                                   pMplsHwVcInfo->u4PwL3Intf);
					DBG_MSG_EXIT (NPAPI_MPLS, CLI_ISS_NP_LOG_DEBUG_LEVEL);
				}
			}
		}
    }
	else
	{
	    /* Create a QOSProfile VPN Map node */
	    pQoSHwVpnProfileMapNode = NpUtilQoSCreateVpnProfileMap (u4VpnId,
                QOS_L2VPN);
        if (pQoSHwVpnProfileMapNode == NULL)
        {
	        /* Add failure trace*/
			return FNP_FAILURE;
		}
	}
    pQoSHwVpnProfileMapNode->u4PwLifId = u4PwVpId;

    DBG_MSG_EXIT (NPAPI_MPLS, CLI_ISS_NP_LOG_DEBUG_LEVEL);
    return FNP_SUCCESS;
}
#endif