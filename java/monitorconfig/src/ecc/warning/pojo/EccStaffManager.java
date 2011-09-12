package ecc.warning.pojo;

import java.sql.ResultSet;
import java.sql.SQLException;

import org.nutz.dao.entity.annotation.Column;
import org.nutz.dao.entity.annotation.Name;
import org.nutz.dao.entity.annotation.Table;

@Table("ecc_staff_manager")
public class EccStaffManager {
	public EccStaffManager(){	}
	public static EccStaffManager getInstance(ResultSet rs) throws SQLException{
		EccStaffManager esm=new EccStaffManager();
		esm.staffId=rs.getString("staff_id");
		esm.staffName=rs.getString("staff_name");
		esm.connNbr=rs.getString("conn_nbr");
		esm.staffNo=rs.getString("staff_no");
		esm.email=rs.getString("e-mail");
		return esm;
		
	}
	@Name
	@Column("staff_id")
	private String staffId;
	@Column("staff_name")
	private String staffName;
	@Column("conn_nbr")
	private String connNbr;
	@Column("staff_no")
	private String staffNo;
	@Column
	private String sts;
	@Column("e-mail")
	private String email;
	
	
	/**
	 * @return the email
	 */
	public String getEmail() {
		return email;
	}
	/**
	 * @param email the email to set
	 */
	public void setEmail(String email) {
		this.email = email;
	}
	public String getSts() {
		return sts;
	}
	public void setSts(String sts) {
		this.sts = sts;
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
	

}
