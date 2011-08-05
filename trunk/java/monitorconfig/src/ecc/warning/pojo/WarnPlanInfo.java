package ecc.warning.pojo;

import java.sql.Date;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

import org.nutz.dao.entity.annotation.Column;
import org.nutz.dao.entity.annotation.Many;
import org.nutz.dao.entity.annotation.Name;
import org.nutz.dao.entity.annotation.Prev;
import org.nutz.dao.entity.annotation.Readonly;
import org.nutz.dao.entity.annotation.SQL;
import org.nutz.dao.entity.annotation.Table;

@Table("warn_plan_info")
public class WarnPlanInfo {
	public WarnPlanInfo(){
		
	}
	public static WarnPlanInfo getInstance(ResultSet rs) throws SQLException{
		WarnPlanInfo warnPlanInfo=new WarnPlanInfo();
		warnPlanInfo.areaCode=rs.getString("area_code");
		warnPlanInfo.planId=rs.getString("plan_id");
		warnPlanInfo.companyId=rs.getString("company_id");
		warnPlanInfo.planName=rs.getString("plan_name");
		warnPlanInfo.remark=rs.getString("remark");
		warnPlanInfo.runCycle=rs.getString("run_cycle");
		warnPlanInfo.runStatus=rs.getString("run_status");
		warnPlanInfo.lastTime=rs.getDate("last_time");
		warnPlanInfo.nextTime=rs.getDate("next_time");
		warnPlanInfo.beginHours=rs.getString("begin_hours");
		warnPlanInfo.endHours=rs.getString("end_hours");
		warnPlanInfo.scriptId=rs.getString("script_id");
		warnPlanInfo.dataTagId=rs.getString("data_Tag_id");
		warnPlanInfo.sts=rs.getString("sts");
		
		return warnPlanInfo;
	}
	@Name
	@Prev( @SQL("select max(to_number(plan_id))+1 from warn_plan_info") )
	@Column("plan_id")
	private String planId;
	@Column("company_id")
	private String companyId;
	@Column("area_code")
	private String areaCode;
	@Column("plan_name")
	private String planName;
	@Column
	private String remark;
	@Column("run_cycle")
	private String runCycle;
	@Column("run_status")
	@Readonly
	private String runStatus;
	@Column("last_time")
	@Readonly
	private Date lastTime;
	@Column("next_time")
	private Date nextTime;
	@Column("begin_hours")
	private String beginHours;
	@Column("end_hours")
	private String endHours;
	@Column("script_id")
	private String scriptId;
	@Column("data_Tag_id")
	private String dataTagId;
	@Column("sts")
	private String sts;
	@Many(target=WarnStaff.class,field="planId")
	private List<WarnStaff> warnStaffList;
	
	/**
	 * @return the warnStaffList
	 */
	public List<WarnStaff> getWarnStaffList() {
		return warnStaffList;
	}
	/**
	 * @param warnStaffList the warnStaffList to set
	 */
	public void setWarnStaffList(List<WarnStaff> warnStaffList) {
		this.warnStaffList = warnStaffList;
	}
	/**
	 * @return the planId
	 */
	public String getPlanId() {
		return planId;
	}
	/**
	 * @param planId the planId to set
	 */
	public void setPlanId(String planId) {
		this.planId = planId;
	}
	/**
	 * @return the companyId
	 */
	public String getCompanyId() {
		return companyId;
	}
	/**
	 * @param companyId the companyId to set
	 */
	public void setCompanyId(String companyId) {
		this.companyId = companyId;
	}
	/**
	 * @return the areaCode
	 */
	public String getAreaCode() {
		return areaCode;
	}
	/**
	 * @param areaCode the areaCode to set
	 */
	public void setAreaCode(String areaCode) {
		this.areaCode = areaCode;
	}
	/**
	 * @return the planName
	 */
	public String getPlanName() {
		return planName;
	}
	/**
	 * @param planName the planName to set
	 */
	public void setPlanName(String planName) {
		this.planName = planName;
	}
	/**
	 * @return the remark
	 */
	public String getRemark() {
		return remark;
	}
	/**
	 * @param remark the remark to set
	 */
	public void setRemark(String remark) {
		this.remark = remark;
	}
	/**
	 * @return the runCycle
	 */
	public String getRunCycle() {
		return runCycle;
	}
	/**
	 * @param runCycle the runCycle to set
	 */
	public void setRunCycle(String runCycle) {
		this.runCycle = runCycle;
	}
	/**
	 * @return the runStatus
	 */
	public String getRunStatus() {
		return runStatus;
	}
	/**
	 * @param runStatus the runStatus to set
	 */
	public void setRunStatus(String runStatus) {
		this.runStatus = runStatus;
	}
	/**
	 * @return the lastTime
	 */
	public Date getLastTime() {
		return lastTime;
	}
	/**
	 * @param lastTime the lastTime to set
	 */
	public void setLastTime(Date lastTime) {
		this.lastTime = lastTime;
	}
	/**
	 * @return the nextTime
	 */
	public Date getNextTime() {
		return nextTime;
	}
	/**
	 * @param nextTime the nextTime to set
	 */
	public void setNextTime(Date nextTime) {
		this.nextTime = nextTime;
	}
	/**
	 * @return the beginHours
	 */
	public String getBeginHours() {
		return beginHours;
	}
	/**
	 * @param beginHours the beginHours to set
	 */
	public void setBeginHours(String beginHours) {
		this.beginHours = beginHours;
	}
	/**
	 * @return the endHours
	 */
	public String getEndHours() {
		return endHours;
	}
	/**
	 * @param endHours the endHours to set
	 */
	public void setEndHours(String endHours) {
		this.endHours = endHours;
	}
	/**
	 * @return the scriptId
	 */
	public String getScriptId() {
		return scriptId;
	}
	/**
	 * @param scriptId the scriptId to set
	 */
	public void setScriptId(String scriptId) {
		this.scriptId = scriptId;
	}
	/**
	 * @return the dataTagId
	 */
	public String getDataTagId() {
		return dataTagId;
	}
	/**
	 * @param dataTagId the dataTagId to set
	 */
	public void setDataTagId(String dataTagId) {
		this.dataTagId = dataTagId;
	}
	/**
	 * @return the sts
	 */
	public String getSts() {
		return sts;
	}
	/**
	 * @param sts the sts to set
	 */
	public void setSts(String sts) {
		this.sts = sts;
	}
	
	
	

}
