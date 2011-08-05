package ecc.warning.pojo;



import org.nutz.dao.entity.annotation.Column;
import org.nutz.dao.entity.annotation.One;
import org.nutz.dao.entity.annotation.PK;
import org.nutz.dao.entity.annotation.Table;

@Table("warn_staff")
@PK({"staffId","planId"})
public class WarnStaff {
	public WarnStaff(){}
	@Column("staff_id")
	private String staffId;
	@One(target=EccStaffManager.class,field="staffId")
	private EccStaffManager eccStaffManger;
	@Column("warn_Level")
	private String warnLevel;
	@Column("plan_Id")
	private String planId;
	@Column
	private String sts;
	@Column("warn_Mode")
	private String warnMode;
	private String staffName;
	private String staffNo;
	private String connNbr;
	
	/**
	 * @return the staffName
	 */
	public String getStaffName() {
		return staffName;
	}
	/**
	 * @param staffName the staffName to set
	 */
	public void setStaffName(String staffName) {
		this.staffName = staffName;
	}
	/**
	 * @return the staffNo
	 */
	public String getStaffNo() {
		return staffNo;
	}
	/**
	 * @param staffNo the staffNo to set
	 */
	public void setStaffNo(String staffNo) {
		this.staffNo = staffNo;
	}
	/**
	 * @return the connNbr
	 */
	public String getConnNbr() {
		return connNbr;
	}
	/**
	 * @param connNbr the connNbr to set
	 */
	public void setConnNbr(String connNbr) {
		this.connNbr = connNbr;
	}
	/**
	 * @return the staffId
	 */
	public String getStaffId() {
		return staffId;
	}
	/**
	 * @param staffId the staffId to set
	 */
	public void setStaffId(String staffId) {
		this.staffId = staffId;
	}
	/**
	 * @return the eccStaffManger
	 */
	public EccStaffManager getEccStaffManger() {
		return eccStaffManger;
	}
	/**
	 * @param eccStaffManger the eccStaffManger to set
	 */
	public void setEccStaffManger(EccStaffManager eccStaffManger) {
		this.eccStaffManger = eccStaffManger;
	}
	/**
	 * @return the warnLevel
	 */
	public String getWarnLevel() {
		return warnLevel;
	}
	/**
	 * @param warnLevel the warnLevel to set
	 */
	public void setWarnLevel(String warnLevel) {
		this.warnLevel = warnLevel;
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
	/**
	 * @return the warnMode
	 */
	public String getWarnMode() {
		return warnMode;
	}
	/**
	 * @param warnMode the warnMode to set
	 */
	public void setWarnMode(String warnMode) {
		this.warnMode = warnMode;
	}
	
	

}
