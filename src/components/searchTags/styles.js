
import { Box } from "@material-ui/core";
import styled from "styled-components";


export const TagBox = styled(Box)`
  display: flex;
  flex-direction: row;
  margin-top: 10px;
`;


export const Tag = styled.p`
  margin-right: 10px;
  color: #6c8799;
  font-weight: 600;
  cursor: pointer;
  &:before {
    content: "#";
    font-weight: 600;
    color: #c2cfd9;
  }
`;


export const OuterBox = styled(Box)`
  display: inline-flex;
  flex-direction: column;
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0px 49px 33px -30px rgba(0, 0, 0, 0.18);
`;


export const SearchIconBox = styled(Box)`
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 55px;
  background-color: #4f70ff;
  color: white;
  border-radius: 10px;
`;